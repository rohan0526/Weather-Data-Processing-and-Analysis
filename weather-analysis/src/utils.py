"""
Utility Functions
Helper functions for weather analysis project
"""

import pandas as pd
import numpy as np
from datetime import datetime


def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit"""
    return (celsius * 9/5) + 32


def fahrenheit_to_celsius(fahrenheit):
    """Convert Fahrenheit to Celsius"""
    return (fahrenheit - 32) * 5/9


def categorize_temperature(temp_celsius):
    """Categorize temperature into descriptive categories"""
    if temp_celsius < 0:
        return 'Freezing'
    elif temp_celsius < 10:
        return 'Cold'
    elif temp_celsius < 20:
        return 'Moderate'
    elif temp_celsius < 30:
        return 'Warm'
    else:
        return 'Hot'


def categorize_rainfall(precipitation_mm):
    """Categorize rainfall intensity"""
    if precipitation_mm == 0:
        return 'No Rain'
    elif precipitation_mm < 2.5:
        return 'Light'
    elif precipitation_mm < 10:
        return 'Moderate'
    elif precipitation_mm < 50:
        return 'Heavy'
    else:
        return 'Very Heavy'


def get_season(month):
    """Get season based on month (Northern Hemisphere)"""
    if month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    elif month in [9, 10, 11]:
        return 'Autumn'
    else:
        return 'Winter'


def calculate_heat_index(temp_celsius, humidity):
    """
    Calculate heat index (feels like temperature)
    Simplified formula
    """
    temp_f = celsius_to_fahrenheit(temp_celsius)
    
    if temp_f < 80:
        return temp_celsius
    
    # Rothfusz regression
    hi = -42.379 + 2.04901523 * temp_f + 10.14333127 * humidity
    hi -= 0.22475541 * temp_f * humidity - 0.00683783 * temp_f**2
    hi -= 0.05481717 * humidity**2 + 0.00122874 * temp_f**2 * humidity
    hi += 0.00085282 * temp_f * humidity**2 - 0.00000199 * temp_f**2 * humidity**2
    
    return fahrenheit_to_celsius(hi)


def calculate_wind_chill(temp_celsius, wind_speed_kmh):
    """
    Calculate wind chill temperature
    Valid for temperatures at or below 10°C and wind speeds above 4.8 km/h
    """
    if temp_celsius > 10 or wind_speed_kmh < 4.8:
        return temp_celsius
    
    # Wind chill formula (metric)
    wind_chill = 13.12 + 0.6215 * temp_celsius
    wind_chill -= 11.37 * (wind_speed_kmh ** 0.16)
    wind_chill += 0.3965 * temp_celsius * (wind_speed_kmh ** 0.16)
    
    return wind_chill


def format_date_range(start_date, end_date):
    """Format date range for display"""
    if isinstance(start_date, str):
        start_date = pd.to_datetime(start_date)
    if isinstance(end_date, str):
        end_date = pd.to_datetime(end_date)
    
    return f"{start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')}"


def get_month_name(month_number):
    """Convert month number to name"""
    months = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    return months.get(month_number, 'Unknown')


def validate_weather_data(df):
    """
    Validate weather data for common issues
    Returns list of validation warnings
    """
    warnings = []
    
    # Check for required columns
    required_cols = ['Date', 'Temperature']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        warnings.append(f"Missing required columns: {missing_cols}")
    
    # Check for null dates
    if df['Date'].isnull().any():
        null_count = df['Date'].isnull().sum()
        warnings.append(f"Found {null_count} null dates")
    
    # Check temperature range
    if 'Temperature' in df.columns:
        if df['Temperature'].min() < -100:
            warnings.append(f"Suspicious minimum temperature: {df['Temperature'].min()}°C")
        if df['Temperature'].max() > 60:
            warnings.append(f"Suspicious maximum temperature: {df['Temperature'].max()}°C")
    
    # Check humidity range
    if 'Humidity' in df.columns:
        if df['Humidity'].min() < 0 or df['Humidity'].max() > 100:
            warnings.append("Humidity values outside valid range (0-100%)")
    
    # Check for duplicate dates
    if df.duplicated(subset=['Date']).any():
        dup_count = df.duplicated(subset=['Date']).sum()
        warnings.append(f"Found {dup_count} duplicate dates")
    
    return warnings


def generate_summary_stats(df, column_name):
    """Generate comprehensive summary statistics for a column"""
    if column_name not in df.columns:
        return None
    
    series = df[column_name].dropna()
    
    stats = {
        'count': len(series),
        'mean': series.mean(),
        'median': series.median(),
        'std': series.std(),
        'min': series.min(),
        'max': series.max(),
        'q25': series.quantile(0.25),
        'q75': series.quantile(0.75),
        'range': series.max() - series.min(),
        'variance': series.var()
    }
    
    return stats


def detect_outliers(df, column_name, method='iqr', threshold=1.5):
    """
    Detect outliers in a column using IQR or Z-score method
    
    Parameters:
    - method: 'iqr' or 'zscore'
    - threshold: multiplier for IQR (default 1.5) or Z-score threshold (default 3)
    """
    if column_name not in df.columns:
        return None
    
    series = df[column_name].dropna()
    
    if method == 'iqr':
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR
        outliers = series[(series < lower_bound) | (series > upper_bound)]
    
    elif method == 'zscore':
        mean = series.mean()
        std = series.std()
        z_scores = np.abs((series - mean) / std)
        outliers = series[z_scores > threshold]
    
    else:
        return None
    
    return outliers


def calculate_moving_average(df, column_name, window=7):
    """Calculate moving average for time series smoothing"""
    if column_name not in df.columns:
        return None
    
    return df[column_name].rolling(window=window, center=True).mean()


def export_summary_report(df, output_file='weather_summary_report.txt'):
    """Export a text summary report"""
    with open(output_file, 'w') as f:
        f.write("=" * 70 + "\n")
        f.write("WEATHER DATA SUMMARY REPORT\n")
        f.write("=" * 70 + "\n\n")
        
        f.write(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write(f"Total Records: {len(df):,}\n")
        f.write(f"Date Range: {df['Date'].min()} to {df['Date'].max()}\n\n")
        
        f.write("COLUMN SUMMARY:\n")
        f.write("-" * 70 + "\n")
        for col in df.columns:
            f.write(f"\n{col}:\n")
            if df[col].dtype in ['int64', 'float64']:
                stats = generate_summary_stats(df, col)
                if stats:
                    f.write(f"  Mean: {stats['mean']:.2f}\n")
                    f.write(f"  Median: {stats['median']:.2f}\n")
                    f.write(f"  Min: {stats['min']:.2f}\n")
                    f.write(f"  Max: {stats['max']:.2f}\n")
                    f.write(f"  Std Dev: {stats['std']:.2f}\n")
            else:
                f.write(f"  Type: {df[col].dtype}\n")
                f.write(f"  Unique Values: {df[col].nunique()}\n")
        
        f.write("\n" + "=" * 70 + "\n")
        f.write("END OF REPORT\n")
        f.write("=" * 70 + "\n")
    
    print(f"✅ Summary report saved to: {output_file}")


if __name__ == "__main__":
    # Test utility functions
    print("Testing utility functions...\n")
    
    print(f"25°C = {celsius_to_fahrenheit(25):.1f}°F")
    print(f"77°F = {fahrenheit_to_celsius(77):.1f}°C")
    print(f"Temperature 25°C is: {categorize_temperature(25)}")
    print(f"Rainfall 5mm is: {categorize_rainfall(5)}")
    print(f"Month 6 is: {get_month_name(6)}")
    print(f"Season for month 6: {get_season(6)}")
    print(f"\nHeat Index at 30°C, 70% humidity: {calculate_heat_index(30, 70):.1f}°C")
    print(f"Wind Chill at 5°C, 20 km/h wind: {calculate_wind_chill(5, 20):.1f}°C")