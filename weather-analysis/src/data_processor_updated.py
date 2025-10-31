"""
Weather Data Processor - Fixed for Your CSV Format
PySpark-based ETL pipeline for weather data
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, year, month, dayofmonth, avg, max as spark_max, 
    min as spark_min, count, when, to_date, round as spark_round
)
from pyspark.sql.types import DoubleType
import os
import sys


class WeatherDataProcessor:
    def __init__(self):
        """Initialize Spark Session"""
        print("🔧 Initializing Spark Session...")
        try:
            self.spark = SparkSession.builder \
                .appName("WeatherAnalysis") \
                .config("spark.driver.memory", "4g") \
                .getOrCreate()
            self.spark.sparkContext.setLogLevel("ERROR")
            print("✅ Spark Session Created Successfully\n")
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)
    
    def load_data(self, path):
        """Load CSV data"""
        print(f"📂 Loading: {path}")
        df = self.spark.read.csv(path, header=True, inferSchema=True)
        print(f"✅ Loaded: {df.count()} rows, {len(df.columns)} columns\n")
        
        # Show column names
        print("📋 Columns found:", df.columns)
        return df
    
    def clean_data(self, df):
        """Clean and transform data"""
        print("\n🧹 Cleaning data...")
        initial = df.count()
        
        # Rename columns to standard names
        column_mapping = {
            'Formatted Date': 'Date',
            'Temperature (C)': 'Temperature',
            'Apparent Temperature (C)': 'Apparent_Temperature',
            'Wind Speed (km/h)': 'Wind_Speed',
            'Wind Bearing (degrees)': 'Wind_Bearing',
            'Visibility (km)': 'Visibility',
            'Loud Cover': 'Cloud_Cover',
            'Pressure (millibars)': 'Pressure',
            'Precip Type': 'Precip_Type',
            'Daily Summary': 'Daily_Summary'
        }
        
        for old_name, new_name in column_mapping.items():
            if old_name in df.columns:
                df = df.withColumnRenamed(old_name, new_name)
                print(f"  Renamed: {old_name} → {new_name}")
        
        # Convert Date - extract just the date part (first 10 chars)
        if 'Date' in df.columns:
            df = df.withColumn('Date', to_date(col('Date').substr(1, 10), 'yyyy-MM-dd'))
        
        # Remove rows with null dates
        df = df.filter(col('Date').isNotNull())
        
        # Fill missing numeric values with mean
        numeric_columns = ['Temperature', 'Apparent_Temperature', 'Humidity', 
                          'Wind_Speed', 'Pressure', 'Visibility']
        
        for col_name in numeric_columns:
            if col_name in df.columns:
                mean_val = df.select(avg(col(col_name))).first()[0]
                if mean_val:
                    df = df.fillna({col_name: mean_val})
                df = df.withColumn(col_name, col(col_name).cast(DoubleType()))
        
        # Remove duplicates
        df = df.dropDuplicates(['Date'])
        
        final = df.count()
        print(f"✅ Cleaned: {final} rows (removed {initial-final})\n")
        return df
    
    def add_features(self, df):
        """Add derived features"""
        print("➕ Adding features...")
        
        # Date features
        df = df.withColumn('Year', year(col('Date')))
        df = df.withColumn('Month', month(col('Date')))
        df = df.withColumn('Day', dayofmonth(col('Date')))
        
        # Season
        df = df.withColumn('Season',
            when((col('Month') >= 3) & (col('Month') <= 5), 'Spring')
            .when((col('Month') >= 6) & (col('Month') <= 8), 'Summer')
            .when((col('Month') >= 9) & (col('Month') <= 11), 'Autumn')
            .otherwise('Winter')
        )
        
        # Temperature category
        if 'Temperature' in df.columns:
            df = df.withColumn('Temp_Category',
                when(col('Temperature') < 0, 'Freezing')
                .when(col('Temperature') < 10, 'Cold')
                .when(col('Temperature') < 20, 'Moderate')
                .when(col('Temperature') < 30, 'Warm')
                .otherwise('Hot')
            )
        
        # Create Precipitation column (0 if no rain)
        # Your dataset may not have precipitation amounts, so we'll use 0
        if 'Precipitation' not in df.columns:
            df = df.withColumn('Precipitation', when(col('Precip_Type').isNotNull(), 2.5).otherwise(0.0))
        
        # Rain category
        df = df.withColumn('Rain_Category',
            when(col('Precipitation') == 0, 'No Rain')
            .when(col('Precipitation') < 2.5, 'Light')
            .when(col('Precipitation') < 10, 'Moderate')
            .when(col('Precipitation') < 50, 'Heavy')
            .otherwise('Very Heavy')
        )
        
        print("✅ Features added\n")
        return df
    
    def show_summary(self, df):
        """Display summary"""
        print("📊 Data Summary:")
        print("="*60)
        df.printSchema()
        print("\nSample data (first 5 rows):")
        df.show(5, truncate=False)
        
        if 'Temperature' in df.columns:
            print("\nTemperature statistics:")
            df.select(
                spark_round(avg('Temperature'), 2).alias('Avg'),
                spark_round(spark_min('Temperature'), 2).alias('Min'),
                spark_round(spark_max('Temperature'), 2).alias('Max')
            ).show()
    
    def save_data(self, df, path):
        """Save to CSV"""
        print(f"💾 Saving: {path}")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        df.toPandas().to_csv(path, index=False)
        print(f"✅ Saved successfully\n")
    
    def stop(self):
        """Stop Spark"""
        self.spark.stop()
        print("🛑 Spark stopped")


def main():
    print("="*60)
    print("🌤️  WEATHER DATA PROCESSOR")
    print("="*60 + "\n")
    
    processor = WeatherDataProcessor()
    
    try:
        # Paths
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        input_path = os.path.join(root, "data", "weather.csv")
        output_path = os.path.join(root, "data", "weather_processed.csv")
        
        print(f"📁 Root: {root}")
        print(f"📁 Input: {input_path}")
        print(f"📁 Output: {output_path}\n")
        
        # Process
        df = processor.load_data(input_path)
        df = processor.clean_data(df)
        df = processor.add_features(df)
        processor.show_summary(df)
        processor.save_data(df, output_path)
        
        print("="*60)
        print("✅ PROCESSING COMPLETE!")
        print("="*60)
        print(f"\n📊 Processed file: {output_path}")
        print("\n🎯 Next steps:")
        print("1. python src\\analysis.py")
        print("2. streamlit run app.py")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        processor.stop()


if __name__ == "__main__":
    main()