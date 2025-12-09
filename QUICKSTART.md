# Quick Start Guide

## Getting Started

### Windows (PowerShell)

1. **Setup (first time only)**
   ```powershell
   .\setup.ps1
   ```

2. **Start the Server**
   ```powershell
   .\start.ps1
   ```

### Linux/Mac

1. **Setup (first time only)**
   ```bash
   chmod +x setup.sh start.sh
   ./setup.sh
   ```

2. **Start the Server**
   ```bash
   ./start.sh
   ```

### Manual Setup

1. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the Server**
   ```bash
   python app.py
   ```

3. **Open in Browser**
   Navigate to: `http://localhost:5000`

4. **Upload Your File**
   - Click the upload area or drag and drop your Excel file
   - The platform will automatically process the file
   - View statistics, charts, and tables

## Testing the Platform

**Make sure virtual environment is activated first!**

Test the data processor with the example file:
```bash
# Windows:
venv\Scripts\activate
python test_processor.py

# Linux/Mac:
source venv/bin/activate
python test_processor.py
```

## Example File

The included `OCTOBER OVERTIME - CN V3 - 27 NOV 2025.xlsx` file contains sample data from June through November 2025 with:
- 6,098 total records
- 34 unique employees
- Multiple sheets (one per month)

## Features Overview

### Upload & Process
- Supports .xlsx and .xls files
- Drag-and-drop or click to upload
- Processes multiple sheets automatically
- Cleans and normalizes data

### Analytics Dashboard
- **Statistics Cards**: Quick overview of totals
- **Monthly Chart**: Bar chart showing overtime by month
- **Daily Trend**: Line chart showing daily overtime patterns
- **Top Employees**: Horizontal bar chart of top performers

### Data Tables
- **By Employee**: Detailed breakdown per employee
- **By Month**: Monthly aggregates
- **Top Employees**: Ranked list of highest overtime

### Export
- Export all summaries to Excel with one click

## Troubleshooting

**Port Already in Use?**
- Change the port in `app.py`: `app.run(port=5001)`

**File Upload Fails?**
- Check file size (max 50MB)
- Ensure file is .xlsx or .xls format
- Verify file structure matches expected format

**Charts Not Displaying?**
- Check browser console for errors
- Ensure JavaScript is enabled
- Try refreshing the page after upload

## Next Steps

- Customize the analysis in `data_processor.py`
- Modify the UI in `templates/index.html` and `static/css/style.css`
- Add additional API endpoints in `app.py`

