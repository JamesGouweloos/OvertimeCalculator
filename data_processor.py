"""
Data processing module for overtime analysis.
Handles reading, cleaning, and processing Excel overtime files.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import re
import calendar


class OvertimeProcessor:
    """Processes and analyzes overtime data from Excel files."""
    
    def __init__(self):
        self.data = None
        self.raw_data = None
    
    def hours_to_hhmmss(self, hours: float) -> str:
        """Convert decimal hours to HH:MM:SS format."""
        if pd.isna(hours) or hours == 0:
            return "00:00:00"
        
        # Handle negative hours
        is_negative = hours < 0
        hours = abs(hours)
        
        total_seconds = int(hours * 3600)
        h = total_seconds // 3600
        m = (total_seconds % 3600) // 60
        s = total_seconds % 60
        
        result = f"{h:02d}:{m:02d}:{s:02d}"
        return f"-{result}" if is_negative else result
    
    def hours_to_ddhhmmss(self, hours: float, hours_per_day: float = 8.0) -> str:
        """Convert decimal hours to DD:HH:MM:SS format (assuming 8 hours per day)."""
        if pd.isna(hours) or hours == 0:
            return "00:00:00:00"
        
        # Handle negative hours
        is_negative = hours < 0
        hours = abs(hours)
        
        days = int(hours // hours_per_day)
        remaining_hours = hours % hours_per_day
        
        total_seconds = int(remaining_hours * 3600)
        h = total_seconds // 3600
        m = (total_seconds % 3600) // 60
        s = total_seconds % 60
        
        result = f"{days:02d}:{h:02d}:{m:02d}:{s:02d}"
        return f"-{result}" if is_negative else result
    
    def load_excel(self, file_path: str) -> Dict[str, pd.DataFrame]:
        """Load Excel file with multiple sheets."""
        try:
            self.raw_data = pd.read_excel(file_path, sheet_name=None)
            return self.raw_data
        except Exception as e:
            raise Exception(f"Error loading Excel file: {str(e)}")
    
    def clean_time_value(self, value) -> Optional[str]:
        """Clean and normalize time values."""
        if pd.isna(value):
            return None
        
        # Handle datetime.time objects directly
        if isinstance(value, pd.Timestamp):
            # Check if it's actually a time (not a datetime)
            if hasattr(value, 'time'):
                time_obj = value.time()
                return time_obj.strftime('%H:%M:%S')
            # Handle invalid dates like 1903-12-31 (Excel date overflow)
            elif value.year < 2000:
                # Try to extract time component from invalid dates
                # These often represent times that overflowed into date
                if value.year == 1903 or value.year == 1900:
                    # Extract time component
                    time_str = value.strftime('%H:%M:%S')
                    # If it's a valid time (not midnight), use it
                    if time_str != '00:00:00':
                        return time_str
                return None
            else:
                return value.strftime('%H:%M:%S')
        
        # Handle datetime.time objects (from pandas)
        if hasattr(value, 'hour') and hasattr(value, 'minute') and hasattr(value, 'second'):
            try:
                return value.strftime('%H:%M:%S')
            except:
                # Fallback for time objects
                try:
                    return f"{value.hour:02d}:{value.minute:02d}:{value.second:02d}"
                except:
                    pass
        
        # Handle datetime objects
        if isinstance(value, datetime):
            # Handle invalid dates like 1903-12-31 (Excel date overflow)
            if value.year < 2000:
                # Try to extract time component from invalid dates
                # These often represent times that overflowed into date
                if value.year == 1903 or value.year == 1900:
                    # Extract time component
                    time_str = value.strftime('%H:%M:%S')
                    # If it's a valid time (not midnight), use it
                    if time_str != '00:00:00':
                        return time_str
                return None
            return value.strftime('%H:%M:%S')
        
        # Convert to string if not already
        value_str = str(value).strip()
        
        # Skip invalid values
        if value_str.lower() in ['off', 'nan', 'none', 'n/a', 'na', '']:
            return None
        
        # Handle time strings
        if ':' in value_str:
            # Extract time pattern HH:MM:SS or HH:MM
            time_match = re.search(r'(\d{1,2}):(\d{2})(?::(\d{2}))?', value_str)
            if time_match:
                hours = int(time_match.group(1))
                minutes = int(time_match.group(2))
                seconds = int(time_match.group(3)) if time_match.group(3) else 0
                
                # Validate time values
                if hours < 0 or hours > 23 or minutes < 0 or minutes > 59 or seconds < 0 or seconds > 59:
                    return None
                
                return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        
        return None
    
    def time_to_hours(self, time_str: Optional[str]) -> float:
        """Convert time string (HH:MM:SS) to decimal hours."""
        if not time_str or pd.isna(time_str):
            return 0.0
        
        try:
            parts = str(time_str).split(':')
            if len(parts) >= 2:
                hours = float(parts[0])
                minutes = float(parts[1])
                seconds = float(parts[2]) if len(parts) > 2 else 0.0
                return hours + (minutes / 60.0) + (seconds / 3600.0)
        except:
            pass
        
        return 0.0
    
    def parse_date(self, date_str) -> Optional[datetime]:
        """Parse date string to datetime object."""
        if pd.isna(date_str):
            return None
        
        # Handle datetime objects directly
        if isinstance(date_str, (datetime, pd.Timestamp)):
            # Skip invalid dates
            if date_str.year < 2000:
                return None
            return date_str
        
        date_str = str(date_str).strip()
        
        # Skip invalid values
        if date_str.lower() in ['off', 'nan', 'none', 'n/a', 'na', '']:
            return None
        
        # Extract date from strings like "2025-10-01 (Mon)" or "2025-10-01"
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', date_str)
        if date_match:
            try:
                parsed_date = pd.to_datetime(date_match.group(1))
                # Validate date is reasonable
                if parsed_date.year >= 2000 and parsed_date.year <= 2100:
                    return parsed_date
            except:
                pass
        
        # Try parsing the whole string
        try:
            parsed_date = pd.to_datetime(date_str)
            # Validate date is reasonable
            if parsed_date.year >= 2000 and parsed_date.year <= 2100:
                return parsed_date
        except:
            pass
        
        return None
    
    def contains_month_name(self, sheet_name: str) -> bool:
        """Check if sheet name contains a valid month name."""
        sheet_lower = sheet_name.lower()
        month_names = [
            'january', 'february', 'march', 'april', 'may', 'june',
            'july', 'august', 'september', 'october', 'november', 'december',
            'jan', 'feb', 'mar', 'apr', 'may', 'jun',
            'jul', 'aug', 'sep', 'sept', 'oct', 'nov', 'dec'
        ]
        return any(month in sheet_lower for month in month_names)
    
    def normalize_month_name(self, sheet_name: str) -> str:
        """Normalize month name from sheet name to standard format (e.g., 'August')."""
        sheet_lower = sheet_name.lower()
        
        # Map of month names and variations to standard names
        month_mapping = {
            'january': 'January', 'jan': 'January',
            'february': 'February', 'feb': 'February',
            'march': 'March', 'mar': 'March',
            'april': 'April', 'apr': 'April',
            'may': 'May',
            'june': 'June', 'jun': 'June',
            'july': 'July', 'jul': 'July',
            'august': 'August', 'aug': 'August',
            'september': 'September', 'sep': 'September', 'sept': 'September',
            'october': 'October', 'oct': 'October',
            'november': 'November', 'nov': 'November',
            'december': 'December', 'dec': 'December'
        }
        
        # Find the month in the sheet name
        for month_key, month_standard in month_mapping.items():
            if month_key in sheet_lower:
                return month_standard
        
        # If no month found, return original (shouldn't happen if filtered correctly)
        return sheet_name
    
    def is_valid_overtime_sheet(self, df: pd.DataFrame) -> bool:
        """Check if a sheet has the required columns for overtime data."""
        required_columns = ['PIN CODE', 'FULL NAME', 'DATE']
        return all(col in df.columns for col in required_columns)
    
    def clean_sheet(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean a single sheet of overtime data."""
        # Skip if not a valid overtime sheet
        if not self.is_valid_overtime_sheet(df):
            return pd.DataFrame()
        
        # Remove unnamed columns
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        
        # Handle missing PIN CODE - assign 1 if missing
        # First, fill NaN values with 1
        df['PIN CODE'] = df['PIN CODE'].fillna(1)
        
        # Convert PIN CODE to numeric, replacing invalid entries with 1
        df['PIN CODE'] = pd.to_numeric(df['PIN CODE'], errors='coerce')
        df['PIN CODE'] = df['PIN CODE'].fillna(1)
        
        # Ensure PIN CODE is integer
        df['PIN CODE'] = df['PIN CODE'].astype(int)
        
        if len(df) == 0:
            return pd.DataFrame()
        
        # Clean date column
        if 'DATE' in df.columns:
            df['DATE'] = df['DATE'].apply(self.parse_date)
            df = df[df['DATE'].notna()]
        
        if len(df) == 0:
            return pd.DataFrame()
        
        # Clean time columns
        time_columns = ['T&A IN', 'T&A OUT', 'T&A BREAK', 'HOURS WORKED', 'OVERTIME HOURS', 'TARGET']
        for col in time_columns:
            if col in df.columns:
                df[col] = df[col].apply(self.clean_time_value)
        
        # Convert hours worked to decimal first
        if 'HOURS WORKED' in df.columns:
            df['HOURS_WORKED_DECIMAL'] = df['HOURS WORKED'].apply(self.time_to_hours)
        else:
            df['HOURS_WORKED_DECIMAL'] = 0.0
        
        # Convert target to decimal
        if 'TARGET' in df.columns:
            df['TARGET_DECIMAL'] = df['TARGET'].apply(self.time_to_hours)
        else:
            df['TARGET_DECIMAL'] = 0.0
        
        # Convert overtime hours to decimal
        # Handle negative times (Excel represents them as dates in 1900s)
        if 'OVERTIME HOURS' in df.columns:
            def parse_overtime(value):
                """Parse overtime, handling negative times represented as 1900s dates."""
                if pd.isna(value):
                    return None  # Return None to indicate missing, will calculate from hours worked
                
                # Check if it's a datetime with year 1900-1903 (negative time indicator in Excel)
                if isinstance(value, (datetime, pd.Timestamp)):
                    if value.year < 2000:
                        # This represents a negative time (under target)
                        # Excel wraps negative times to show dates like 1903-12-31 22:57:17
                        # Calculate the actual negative time: 24:00:00 - displayed_time
                        time_str = value.strftime('%H:%M:%S')
                        if time_str != '00:00:00':
                            # Convert to hours and subtract from 24 to get negative
                            wrapped_hours = self.time_to_hours(time_str)
                            negative_hours = wrapped_hours - 24.0
                            return negative_hours
                        return None
                
                # Handle time objects that might be from datetime parsing
                if hasattr(value, 'hour') and hasattr(value, 'minute'):
                    # This is a time object, parse normally
                    time_str = self.clean_time_value(value)
                    if time_str:
                        hours = self.time_to_hours(time_str)
                        # If time is > 12 hours, it's likely a wrapped negative time
                        # (Excel shows negative times as 24 - abs(negative_time))
                        if hours > 12:
                            # Calculate negative: wrapped_time - 24
                            return hours - 24.0
                        return hours
                
                # Normal time string parsing
                time_str = self.clean_time_value(value)
                if time_str:
                    hours = self.time_to_hours(time_str)
                    # If time is > 12 hours, it's likely a wrapped negative time
                    if hours > 12:
                        # Calculate negative: wrapped_time - 24
                        return hours - 24.0
                    return hours
                return None
            
            df['OVERTIME_HOURS_DECIMAL'] = df['OVERTIME HOURS'].apply(parse_overtime)
            
            # Calculate overtime from hours worked vs target for missing or validation
            calculated_overtime = df['HOURS_WORKED_DECIMAL'] - df['TARGET_DECIMAL']
            
            # Fill missing overtime with calculated value
            mask_missing = df['OVERTIME_HOURS_DECIMAL'].isna()
            df.loc[mask_missing, 'OVERTIME_HOURS_DECIMAL'] = calculated_overtime[mask_missing]
            
            # Replace suspiciously high overtime values (> 12 hours) with calculated
            # These are likely Excel date wrapping issues
            # But preserve negative values - only replace if suspiciously high positive
            mask_suspicious = df['OVERTIME_HOURS_DECIMAL'] > 12
            df.loc[mask_suspicious, 'OVERTIME_HOURS_DECIMAL'] = calculated_overtime[mask_suspicious]
        else:
            # Calculate overtime from hours worked vs target (allows negative)
            df['OVERTIME_HOURS_DECIMAL'] = df['HOURS_WORKED_DECIMAL'] - df['TARGET_DECIMAL']
        
        return df.reset_index(drop=True)
    
    def process_all_sheets(self, file_path: str) -> pd.DataFrame:
        """Process all sheets and combine into single dataframe."""
        sheets = self.load_excel(file_path)
        cleaned_sheets = []
        skipped_sheets = []
        
        for sheet_name, df in sheets.items():
            # Skip sheets that don't contain month names
            if not self.contains_month_name(sheet_name):
                skipped_sheets.append(sheet_name)
                continue
            
            try:
                cleaned_df = self.clean_sheet(df.copy())
                if len(cleaned_df) > 0:
                    # Normalize month name
                    normalized_month = self.normalize_month_name(sheet_name)
                    cleaned_df['MONTH'] = normalized_month
                    cleaned_sheets.append(cleaned_df)
                else:
                    skipped_sheets.append(sheet_name)
            except Exception as e:
                # Log but continue processing other sheets
                print(f"Warning: Skipping sheet '{sheet_name}': {str(e)}")
                skipped_sheets.append(sheet_name)
                continue
        
        if len(cleaned_sheets) == 0:
            raise ValueError("No valid overtime data found in any sheet. Please check the file format.")
        
        self.data = pd.concat(cleaned_sheets, ignore_index=True)
        
        if skipped_sheets:
            print(f"Note: Skipped {len(skipped_sheets)} sheet(s) (no month name found): {', '.join(skipped_sheets)}")
        
        return self.data
    
    def get_summary_by_employee(self) -> pd.DataFrame:
        """Get summary statistics by employee."""
        if self.data is None:
            raise ValueError("No data loaded. Call process_all_sheets() first.")
        
        summary = self.data.groupby(['PIN CODE', 'FULL NAME']).agg({
            'OVERTIME_HOURS_DECIMAL': ['sum', 'mean', 'count'],
            'HOURS_WORKED_DECIMAL': 'sum',
            'DATE': ['min', 'max']
        }).reset_index()
        
        summary.columns = ['PIN_CODE', 'FULL_NAME', 'TOTAL_OVERTIME_HOURS', 
                          'AVG_OVERTIME_HOURS', 'DAYS_WORKED', 
                          'TOTAL_HOURS_WORKED', 'FIRST_DATE', 'LAST_DATE']
        
        # Add formatted time columns
        summary['TOTAL_OVERTIME_HHMMSS'] = summary['TOTAL_OVERTIME_HOURS'].apply(self.hours_to_hhmmss)
        summary['TOTAL_OVERTIME_DDHHMMSS'] = summary['TOTAL_OVERTIME_HOURS'].apply(self.hours_to_ddhhmmss)
        summary['AVG_OVERTIME_HHMMSS'] = summary['AVG_OVERTIME_HOURS'].apply(self.hours_to_hhmmss)
        summary['AVG_OVERTIME_DDHHMMSS'] = summary['AVG_OVERTIME_HOURS'].apply(self.hours_to_ddhhmmss)
        
        return summary.sort_values('TOTAL_OVERTIME_HOURS', ascending=False)
    
    def get_summary_by_month(self) -> pd.DataFrame:
        """Get summary statistics by month."""
        if self.data is None:
            raise ValueError("No data loaded. Call process_all_sheets() first.")
        
        summary = self.data.groupby('MONTH').agg({
            'OVERTIME_HOURS_DECIMAL': ['sum', 'mean', 'count'],
            'HOURS_WORKED_DECIMAL': 'sum',
            'PIN CODE': 'nunique'
        }).reset_index()
        
        summary.columns = ['MONTH', 'TOTAL_OVERTIME_HOURS', 'AVG_OVERTIME_HOURS', 
                          'TOTAL_RECORDS', 'TOTAL_HOURS_WORKED', 'UNIQUE_EMPLOYEES']
        
        # Add formatted time columns
        summary['TOTAL_OVERTIME_HHMMSS'] = summary['TOTAL_OVERTIME_HOURS'].apply(self.hours_to_hhmmss)
        summary['TOTAL_OVERTIME_DDHHMMSS'] = summary['TOTAL_OVERTIME_HOURS'].apply(self.hours_to_ddhhmmss)
        summary['AVG_OVERTIME_HHMMSS'] = summary['AVG_OVERTIME_HOURS'].apply(self.hours_to_hhmmss)
        summary['AVG_OVERTIME_DDHHMMSS'] = summary['AVG_OVERTIME_HOURS'].apply(self.hours_to_ddhhmmss)
        
        return summary
    
    def get_employee_details(self, pin_code: Optional[int] = None, 
                            name: Optional[str] = None) -> pd.DataFrame:
        """Get detailed records for a specific employee."""
        if self.data is None:
            raise ValueError("No data loaded. Call process_all_sheets() first.")
        
        filtered = self.data.copy()
        
        if pin_code:
            filtered = filtered[filtered['PIN CODE'] == pin_code]
        
        if name:
            filtered = filtered[filtered['FULL NAME'].str.contains(name, case=False, na=False)]
        
        return filtered.sort_values('DATE')
    
    def get_daily_totals(self) -> pd.DataFrame:
        """Get daily totals across all employees."""
        if self.data is None:
            raise ValueError("No data loaded. Call process_all_sheets() first.")
        
        daily = self.data.groupby('DATE').agg({
            'OVERTIME_HOURS_DECIMAL': 'sum',
            'HOURS_WORKED_DECIMAL': 'sum',
            'PIN CODE': 'nunique'
        }).reset_index()
        
        daily.columns = ['DATE', 'TOTAL_OVERTIME_HOURS', 'TOTAL_HOURS_WORKED', 'EMPLOYEES_COUNT']
        
        return daily.sort_values('DATE')
    
    def get_top_overtime_employees(self, n: int = 10) -> pd.DataFrame:
        """Get top N employees by total overtime hours."""
        summary = self.get_summary_by_employee()
        return summary.head(n)
    
    def export_summary(self, output_path: str):
        """Export summary data to Excel."""
        if self.data is None:
            raise ValueError("No data loaded. Call process_all_sheets() first.")
        
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            self.get_summary_by_employee().to_excel(writer, sheet_name='By Employee', index=False)
            self.get_summary_by_month().to_excel(writer, sheet_name='By Month', index=False)
            self.get_daily_totals().to_excel(writer, sheet_name='Daily Totals', index=False)
            self.get_top_overtime_employees(20).to_excel(writer, sheet_name='Top 20 Employees', index=False)

