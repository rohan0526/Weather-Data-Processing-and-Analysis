"""
Weather Data Analysis - Fixed for Pandas 2.x
Statistical analysis and insights generation
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, avg, max as spark_max, min as spark_min, 
    sum as spark_sum, count, round as spark_round, stddev, when
)
import pandas as pd
import os


class WeatherAnalyzer:
    def __init__(self):
        """Initialize Spark"""
        print("🔧 Initializing Spark...")
        self.spark = SparkSession.builder \
            .appName("WeatherAnalysis") \
            .config("spark.driver.memory", "4g") \
            .config("spark.sql.execution.arrow.pyspark.enabled", "false") \
            .getOrCreate()
        self.spark.sparkContext.setLogLevel("ERROR")
        print("✅ Spark initialized\n")
    
    def load_data(self, path):
        """Load processed data"""
        print(f"📂 Loading: {path}")
        df = self.spark.read.csv(path, header=True, inferSchema=True)
        # Convert Date to string to avoid pandas datetime issues
        df = df.withColumn('Date', col('Date').cast('string'))
        print(f"✅ Loaded: {df.count()} records\n")
        return df
    
    def yearly_trends(self, df):
        """Yearly temperature trends"""
        print("📈 Yearly trends...")
        result = df.groupBy('Year').agg(
            spark_round(avg('Temperature'), 2).alias('Avg_Temperature'),
            spark_round(spark_max('Temperature'), 2).alias('Max_Temperature'),
            spark_round(spark_min('Temperature'), 2).alias('Min_Temperature'),
            count('*').alias('Record_Count')
        ).orderBy('Year')
        result.show()
        return result.toPandas()
    
    def monthly_trends(self, df):
        """Monthly temperature trends"""
        print("📅 Monthly trends...")
        result = df.groupBy('Year', 'Month').agg(
            spark_round(avg('Temperature'), 2).alias('Avg_Temperature'),
            spark_round(spark_max('Temperature'), 2).alias('Max_Temperature'),
            spark_round(spark_min('Temperature'), 2).alias('Min_Temperature')
        ).orderBy('Year', 'Month')
        result.show(12)
        return result.toPandas()
    
    def seasonal_patterns(self, df):
        """Seasonal analysis"""
        print("🍂 Seasonal patterns...")
        result = df.groupBy('Season').agg(
            spark_round(avg('Temperature'), 2).alias('Avg_Temperature'),
            spark_round(avg('Humidity'), 2).alias('Avg_Humidity'),
            spark_round(avg('Wind_Speed'), 2).alias('Avg_Wind_Speed'),
            spark_round(spark_sum('Precipitation'), 2).alias('Total_Precipitation'),
            count('*').alias('Record_Count')
        ).orderBy(
            when(col('Season') == 'Spring', 1)
            .when(col('Season') == 'Summer', 2)
            .when(col('Season') == 'Autumn', 3)
            .otherwise(4)
        )
        result.show()
        return result.toPandas()
    
    def rainfall_patterns(self, df):
        """Rainfall analysis"""
        print("🌧️ Rainfall patterns...")
        result = df.groupBy('Year', 'Month').agg(
            spark_round(spark_sum('Precipitation'), 2).alias('Total_Precipitation'),
            spark_round(avg('Precipitation'), 2).alias('Avg_Daily_Precipitation'),
            count(when(col('Precipitation') > 0, True)).alias('Rainy_Days')
        ).orderBy('Year', 'Month')
        result.show(12)
        return result.toPandas()
    
    def extreme_events(self, df):
        """Identify extremes"""
        print("⚠️ Extreme events...")
        
        # Hottest days
        hottest = df.orderBy(col('Temperature').desc()).limit(10)
        print("\n🔥 Top 10 Hottest Days:")
        hottest.select('Date', 'Temperature', 'Humidity').show()
        
        # Coldest days
        coldest = df.orderBy(col('Temperature').asc()).limit(10)
        print("\n❄️ Top 10 Coldest Days:")
        coldest.select('Date', 'Temperature', 'Humidity').show()
        
        # Heaviest rainfall days
        rainiest = df.orderBy(col('Precipitation').desc()).limit(10)
        print("\n🌊 Top 10 Rainiest Days:")
        rainiest.select('Date', 'Precipitation', 'Temperature').show()
        
        # Return None to avoid pandas conversion issues
        # We already displayed the data above
        return {
            'hottest': None,
            'coldest': None,
            'rainiest': None
        }
    
    def temp_distribution(self, df):
        """Temperature distribution"""
        print("📊 Temperature distribution...")
        result = df.groupBy('Temp_Category').agg(
            count('*').alias('Count'),
            spark_round(avg('Temperature'), 2).alias('Avg_Temperature')
        ).orderBy('Avg_Temperature')
        result.show()
        return result.toPandas()
    
    def correlations(self, df):
        """Correlation analysis"""
        print("🔗 Correlations...")
        
        # Select numeric columns for correlation
        numeric_df = df.select('Temperature', 'Humidity', 'Wind_Speed', 
                               'Precipitation', 'Pressure')
        
        # Convert to pandas
        pandas_df = numeric_df.toPandas()
        corr_matrix = pandas_df.corr()
        
        print("\nCorrelation Matrix:")
        print(corr_matrix)
        return corr_matrix
    
    def summary_report(self, df):
        """Generate summary"""
        print("\n" + "="*60)
        print("📋 WEATHER ANALYSIS REPORT")
        print("="*60)
        
        total = df.count()
        date_stats = df.agg(
            spark_min('Date').alias('Start'),
            spark_max('Date').alias('End')
        ).first()
        
        print(f"\n📅 Records: {total:,}")
        print(f"📅 Range: {date_stats['Start']} to {date_stats['End']}")
        
        temp_stats = df.agg(
            spark_round(avg('Temperature'), 2).alias('Avg'),
            spark_round(spark_min('Temperature'), 2).alias('Min'),
            spark_round(spark_max('Temperature'), 2).alias('Max'),
            spark_round(stddev('Temperature'), 2).alias('StdDev')
        ).first()
        
        print(f"\n🌡️ Temperature:")
        print(f"  Average: {temp_stats['Avg']}°C")
        print(f"  Min: {temp_stats['Min']}°C")
        print(f"  Max: {temp_stats['Max']}°C")
        print(f"  StdDev: {temp_stats['StdDev']}°C")
        
        precip_stats = df.agg(
            spark_round(spark_sum('Precipitation'), 2).alias('Total'),
            spark_round(avg('Precipitation'), 2).alias('Avg'),
            count(when(col('Precipitation') > 0, True)).alias('Rainy_Days')
        ).first()
        
        print(f"\n🌧️ Precipitation:")
        print(f"  Total: {precip_stats['Total']} mm")
        print(f"  Avg Daily: {precip_stats['Avg']} mm")
        print(f"  Rainy Days: {precip_stats['Rainy_Days']}")
        
        print("="*60)
    
    def save_results(self, results, output_dir):
        """Save analysis results"""
        os.makedirs(output_dir, exist_ok=True)
        print(f"\n💾 Saving to: {output_dir}")
        
        for name, df in results.items():
            if df is not None and not df.empty:
                path = os.path.join(output_dir, f"{name}.csv")
                df.to_csv(path, index=False)
                print(f"✅ {name}.csv")
    
    def stop(self):
        """Stop Spark"""
        self.spark.stop()


def main():
    print("="*60)
    print("🌤️  WEATHER DATA ANALYSIS")
    print("="*60 + "\n")
    
    analyzer = WeatherAnalyzer()
    
    try:
        # Paths
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        input_path = os.path.join(root, "data", "weather_processed.csv")
        output_dir = os.path.join(root, "data", "analysis_results")
        
        # Load and analyze
        df = analyzer.load_data(input_path)
        
        yearly = analyzer.yearly_trends(df)
        monthly = analyzer.monthly_trends(df)
        seasonal = analyzer.seasonal_patterns(df)
        rainfall = analyzer.rainfall_patterns(df)
        extremes = analyzer.extreme_events(df)  # Just displays, doesn't return data
        temp_dist = analyzer.temp_distribution(df)
        corr = analyzer.correlations(df)
        
        analyzer.summary_report(df)
        
        # Save results (skip extremes since it's None)
        results = {
            'yearly_trends': yearly,
            'monthly_trends': monthly,
            'seasonal_patterns': seasonal,
            'rainfall_patterns': rainfall,
            'temperature_distribution': temp_dist,
            'correlation_matrix': corr
        }
        
        analyzer.save_results(results, output_dir)
        
        print("\n" + "="*60)
        print("✅ ANALYSIS COMPLETE!")
        print("="*60)
        print(f"\n📊 Results saved to: {output_dir}")
        print("\n🎯 Next: streamlit run app.py")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        analyzer.stop()


if __name__ == "__main__":
    main()