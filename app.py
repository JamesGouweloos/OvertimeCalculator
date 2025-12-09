"""
Flask web application for overtime analysis platform.
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from data_processor import OvertimeProcessor
import json
from datetime import datetime

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Global processor instance
processor = OvertimeProcessor()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Main page."""
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Upload and process Excel file."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        try:
            file.save(filepath)
        except Exception as e:
            return jsonify({'error': f'Error saving file: {str(e)}'}), 500
        
        try:
            # Reset processor state
            processor.data = None
            processor.raw_data = None
            
            # Process the file
            processor.process_all_sheets(filepath)
            
            if processor.data is None or len(processor.data) == 0:
                return jsonify({'error': 'No valid overtime data found in the file. Please check the file format.'}), 400
            
            return jsonify({
                'success': True,
                'message': 'File processed successfully',
                'filename': filename,
                'records': len(processor.data)
            })
        except ValueError as e:
            # User-friendly error for data format issues
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            import traceback
            error_details = str(e)
            # Provide more helpful error messages
            if 'No valid overtime data' in error_details:
                return jsonify({'error': error_details}), 400
            return jsonify({'error': f'Error processing file: {error_details}'}), 500
    
    return jsonify({'error': 'Invalid file type. Please upload .xlsx or .xls files.'}), 400

@app.route('/api/summary/employees', methods=['GET'])
def get_employee_summary():
    """Get summary by employee."""
    try:
        summary = processor.get_summary_by_employee()
        # Convert to JSON-serializable format
        result = summary.to_dict('records')
        return jsonify({'success': True, 'data': result})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Error generating summary: {str(e)}'}), 500

@app.route('/api/summary/month', methods=['GET'])
def get_month_summary():
    """Get summary by month."""
    try:
        summary = processor.get_summary_by_month()
        result = summary.to_dict('records')
        return jsonify({'success': True, 'data': result})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Error generating summary: {str(e)}'}), 500

@app.route('/api/summary/daily', methods=['GET'])
def get_daily_summary():
    """Get daily totals."""
    try:
        daily = processor.get_daily_totals()
        # Convert dates to strings for JSON serialization
        daily['DATE'] = daily['DATE'].dt.strftime('%Y-%m-%d')
        result = daily.to_dict('records')
        return jsonify({'success': True, 'data': result})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Error generating summary: {str(e)}'}), 500

@app.route('/api/employee/<int:pin_code>', methods=['GET'])
def get_employee_details(pin_code):
    """Get details for a specific employee by PIN code."""
    try:
        details = processor.get_employee_details(pin_code=pin_code)
        # Convert dates to strings
        if 'DATE' in details.columns:
            details['DATE'] = details['DATE'].dt.strftime('%Y-%m-%d')
        result = details.to_dict('records')
        return jsonify({'success': True, 'data': result})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Error fetching employee details: {str(e)}'}), 500

@app.route('/api/top-employees', methods=['GET'])
def get_top_employees():
    """Get top employees by overtime."""
    try:
        n = request.args.get('n', 10, type=int)
        top = processor.get_top_overtime_employees(n)
        result = top.to_dict('records')
        return jsonify({'success': True, 'data': result})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Error fetching top employees: {str(e)}'}), 500

@app.route('/api/export', methods=['GET'])
def export_summary():
    """Export summary to Excel."""
    try:
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'summary_export.xlsx')
        processor.export_summary(output_path)
        return send_file(output_path, as_attachment=True, download_name='overtime_summary.xlsx')
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Error exporting summary: {str(e)}'}), 500

@app.route('/api/stats', methods=['GET'])
def get_overall_stats():
    """Get overall statistics."""
    try:
        if processor.data is None:
            return jsonify({'error': 'No data loaded'}), 400
        
        total_overtime = processor.data['OVERTIME_HOURS_DECIMAL'].sum()
        total_hours = processor.data['HOURS_WORKED_DECIMAL'].sum()
        unique_employees = processor.data['PIN CODE'].nunique()
        total_records = len(processor.data)
        avg_overtime = processor.data['OVERTIME_HOURS_DECIMAL'].mean()
        
        stats = {
            'total_overtime_hours': round(total_overtime, 2),
            'total_overtime_hhmmss': processor.hours_to_hhmmss(total_overtime),
            'total_overtime_ddhhmmss': processor.hours_to_ddhhmmss(total_overtime),
            'total_hours_worked': round(total_hours, 2),
            'unique_employees': int(unique_employees),
            'total_records': int(total_records),
            'average_overtime_per_record': round(avg_overtime, 2),
            'average_overtime_hhmmss': processor.hours_to_hhmmss(avg_overtime),
            'average_overtime_ddhhmmss': processor.hours_to_ddhhmmss(avg_overtime)
        }
        
        return jsonify({'success': True, 'data': stats})
    except Exception as e:
        return jsonify({'error': f'Error calculating stats: {str(e)}'}), 500

if __name__ == '__main__':
    # For local development
    app.run(debug=True, host='0.0.0.0', port=5000)

