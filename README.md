# Overtime Analysis Platform

A comprehensive web-based platform for processing and analyzing staff overtime data from Excel spreadsheets.

## Features

- **File Upload**: Upload Excel files (.xlsx, .xls) containing overtime data
- **Data Processing**: Automatically processes multiple sheets and cleans data
- **Visual Analytics**: Interactive charts showing:
  - Overtime by month
  - Daily overtime trends
  - Top employees by overtime hours
- **Data Tables**: View detailed summaries:
  - By employee (total overtime, averages, days worked)
  - By month (monthly totals and averages)
  - Top performers
- **Statistics Dashboard**: Overall statistics including:
  - Total overtime hours
  - Total hours worked
  - Number of unique employees
  - Total records processed
- **Export Functionality**: Export summary reports to Excel

## Installation

1. Install Python 3.8 or higher

2. **Windows (PowerShell):**
   ```powershell
   .\setup.ps1
   ```

   **Linux/Mac:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

   **Manual setup:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

## Usage

**Windows (PowerShell):**
```powershell
.\start.ps1
```

**Linux/Mac:**
```bash
./start.sh
```

**Manual start:**
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Upload an Excel file containing overtime data

4. View the analysis results, charts, and tables

## Data Format

The platform expects Excel files with the following columns:
- PIN CODE: Employee identification number
- FULL NAME: Employee full name
- DATE: Date of work (format: YYYY-MM-DD)
- T&A IN: Time and attendance clock-in time
- T&A OUT: Time and attendance clock-out time
- T&A BREAK: Break duration
- HOURS WORKED: Total hours worked
- OVERTIME HOURS: Overtime hours
- TARGET: Target hours for the day

The platform can process multiple sheets in a single Excel file (e.g., one sheet per month).

## API Endpoints

- `POST /api/upload` - Upload and process Excel file
- `GET /api/stats` - Get overall statistics
- `GET /api/summary/employees` - Get summary by employee
- `GET /api/summary/month` - Get summary by month
- `GET /api/summary/daily` - Get daily totals
- `GET /api/top-employees?n=10` - Get top N employees
- `GET /api/employee/<pin_code>` - Get details for specific employee
- `GET /api/export` - Export summary to Excel

## Project Structure

```
OvertimeCalculator/
├── app.py                 # Flask web application
├── data_processor.py      # Data processing module
├── test_processor.py      # Test script for data processor
├── requirements.txt       # Python dependencies
├── setup.ps1             # Windows setup script
├── start.ps1             # Windows start script
├── setup.sh              # Linux/Mac setup script
├── start.sh              # Linux/Mac start script
├── README.md             # This file
├── QUICKSTART.md         # Quick start guide
├── .gitignore            # Git ignore file
├── venv/                 # Virtual environment (created by setup)
├── templates/
│   └── index.html        # Main web interface
├── static/
│   ├── css/
│   │   └── style.css    # Stylesheet
│   └── js/
│       └── app.js       # Frontend JavaScript
└── uploads/              # Uploaded files storage
```

## Notes

- The platform automatically handles data cleaning, including:
  - Removing invalid dates
  - Normalizing time formats
  - Converting time values to decimal hours
  - Handling multiple sheet formats

- Uploaded files are stored in the `uploads/` directory

- The platform supports drag-and-drop file uploads

## Deployment

For deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md) or [FIREBASE_DEPLOYMENT.md](FIREBASE_DEPLOYMENT.md).

**Quick Deploy Options:**
- **Firebase App Hosting** ⭐ (Current): See `FIREBASE_DEPLOYMENT.md` and `apphosting.yaml`
- **Render**: Free tier, easy setup - see `render.yaml`
- **Railway**: Free trial, auto-detects Flask - see `railway.json`
- **PythonAnywhere**: Free tier, Python-focused
- **VPS**: Full control with Gunicorn + Nginx

## License

This project is provided as-is for overtime analysis purposes.

