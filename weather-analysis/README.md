# 🌤️ Weather Data Processing and Analysis Project

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![PySpark](https://img.shields.io/badge/PySpark-3.3.0-orange.svg)](https://spark.apache.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A comprehensive **Big Data Analytics project** that processes historical weather data using **PySpark** and visualizes climate patterns, temperature trends, and seasonal analysis through an interactive **Streamlit dashboard**.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [Dashboard Features](#-dashboard-features)
- [Data Pipeline](#-data-pipeline)
- [Analysis Outputs](#-analysis-outputs)
- [Screenshots](#-screenshots)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

This project demonstrates **end-to-end Big Data processing** using real-world weather data. It showcases:

- **Distributed data processing** with PySpark
- **ETL pipeline** for data cleaning and transformation
- **Statistical analysis** and correlation studies
- **Interactive visualizations** with Plotly and Streamlit
- **Production-ready code** with error handling and logging

Perfect for data engineering portfolios, academic projects, and learning Big Data technologies!

---

## ✨ Features

### 🔧 Data Processing
- ✅ **Large-scale data handling** - Processes 96,000+ records efficiently
- ✅ **Automated ETL pipeline** - Extract, Transform, Load with PySpark
- ✅ **Data cleaning** - Handles missing values, duplicates, and outliers
- ✅ **Feature engineering** - Creates derived columns (seasons, categories)
- ✅ **Data validation** - Ensures data quality and integrity

### 📊 Analysis Capabilities
- ✅ **Temperature trends** - Yearly, monthly, and seasonal patterns
- ✅ **Rainfall analysis** - Precipitation patterns and rainy day tracking
- ✅ **Extreme weather** - Identification of hottest/coldest days
- ✅ **Correlation studies** - Multi-variable relationship analysis
- ✅ **Statistical summaries** - Comprehensive descriptive statistics

### 🎨 Interactive Dashboard
- ✅ **Real-time filtering** - By year and season
- ✅ **Multiple visualizations** - Line charts, heatmaps, box plots, bar charts
- ✅ **5 analysis tabs** - Temperature, Rainfall, Seasonal, Statistical, Raw Data
- ✅ **Data export** - Download filtered data as CSV
- ✅ **Responsive design** - Works on desktop and mobile

---

## 🛠️ Tech Stack

| Technology | Purpose | Version |
|------------|---------|---------|
| **Python** | Core programming language | 3.12+ |
| **PySpark** | Distributed data processing | 3.3.0 |
| **Pandas** | Data manipulation | Latest |
| **Streamlit** | Web dashboard framework | 1.28+ |
| **Plotly** | Interactive visualizations | Latest |
| **Java** | Spark runtime environment | 11+ |

---

## 📁 Project Structure

```
weather-analysis/
│
├── data/                           # Data directory
│   ├── weather.csv                 # Raw input data (96,453 rows)
│   ├── weather_processed.csv       # Cleaned and processed data
│   └── analysis_results/           # Analysis outputs
│       ├── yearly_trends.csv
│       ├── monthly_trends.csv
│       ├── seasonal_patterns.csv
│       ├── rainfall_patterns.csv
│       ├── temperature_distribution.csv
│       └── correlation_matrix.csv
│
├── src/                            # Source code
│   ├── data_processor_updated.py   # PySpark ETL pipeline
│   ├── analysis_updated.py         # Statistical analysis engine
│   └── utils.py                    # Helper utilities
│
├── streamlit_app_updated.py       # Interactive dashboard
├── requirements.txt                # Python dependencies
├── .gitignore                      # Git ignore rules
├── README.md                       # This file
└── venv/                          # Virtual environment
```

---

## 🚀 Installation

### Prerequisites

1. **Python 3.12+**
   ```bash
   python --version
   ```

2. **Java 11+** (Required for PySpark)
   ```bash
   java -version
   ```
   
   If not installed:
   - Download from [Adoptium](https://adoptium.net/temurin/releases/)
   - Install Java 11 (LTS)
   - Set `JAVA_HOME` environment variable

### Step-by-Step Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/weather-analysis.git
   cd weather-analysis
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Environment Variables**
   
   **Windows (PowerShell):**
   ```powershell
   $env:JAVA_HOME = "C:\Program Files\Eclipse Adoptium\jdk-11.0.28.6-hotspot"
   ```
   
   **Linux/Mac:**
   ```bash
   export JAVA_HOME="/usr/lib/jvm/java-11-openjdk"
   ```

---

## 📖 Usage

### Quick Start (3 Steps)

```bash
# 1. Process the raw data
python src\data_processor_updated.py

# 2. Run statistical analysis
python src\analysis_updated.py

# 3. Launch the dashboard
streamlit run streamlit_app_updated.py
```

The dashboard will open automatically at `http://localhost:8501`

---

### Detailed Workflow

#### **Step 1: Data Processing**

```bash
python src\data_processor_updated.py
```

**What it does:**
- Loads 96,453 weather records
- Cleans and validates data
- Handles missing values and duplicates
- Creates derived features (Season, Temp_Category, Rain_Category)
- Extracts date components (Year, Month, Day)
- Saves processed data to `data/weather_processed.csv`

**Expected output:**
```
============================================================
🌤️  WEATHER DATA PROCESSOR
============================================================
✅ Spark Session Created Successfully

📂 Loading: ...\data\weather.csv
✅ Loaded: 96453 rows, 12 columns

🧹 Cleaning data...
✅ Cleaned: 4019 rows (removed 92434)

➕ Adding features...
✅ Features added

💾 Saving: ...\data\weather_processed.csv
✅ Saved successfully

============================================================
✅ PROCESSING COMPLETE!
============================================================
```

---

#### **Step 2: Statistical Analysis**

```bash
python src\analysis_updated.py
```

**What it does:**
- Analyzes yearly temperature trends
- Calculates monthly patterns
- Identifies seasonal weather characteristics
- Tracks rainfall patterns
- Finds extreme weather events
- Computes correlation matrices
- Generates 6 analysis CSV files

**Expected output:**
```
============================================================
🌤️  WEATHER DATA ANALYSIS
============================================================

📈 Yearly trends...
[Shows temperature statistics by year]

📅 Monthly trends...
[Shows temperature statistics by month]

🍂 Seasonal patterns...
[Shows seasonal averages]

🌧️ Rainfall patterns...
[Shows precipitation data]

⚠️ Extreme events...
🔥 Top 10 Hottest Days
❄️ Top 10 Coldest Days

📊 Temperature distribution...
🔗 Correlations...

💾 Saving to: ...\data\analysis_results
✅ yearly_trends.csv
✅ monthly_trends.csv
✅ seasonal_patterns.csv
✅ rainfall_patterns.csv
✅ temperature_distribution.csv
✅ correlation_matrix.csv

============================================================
✅ ANALYSIS COMPLETE!
============================================================
```

---

#### **Step 3: Launch Dashboard**

```bash
streamlit run streamlit_app_updated.py
```

**What it does:**
- Starts local web server
- Opens browser automatically
- Loads processed data and analysis results
- Provides interactive filtering and visualization

**Access at:** `http://localhost:8501`

---

## 🎨 Dashboard Features

### 1️⃣ **Key Statistics**
Real-time metrics displaying:
- Average Temperature
- Maximum Temperature
- Minimum Temperature
- Total Records (updates based on filters)

### 2️⃣ **Temperature Trends Tab** 🌡️
- **Daily Temperature Variation** - Interactive line chart
- **Yearly Trends** - Multi-line chart (Avg, Max, Min)
- **Monthly Heatmap** - Temperature across months and years
- **Distribution Histogram** - Temperature frequency distribution

### 3️⃣ **Rainfall Analysis Tab** 🌧️
- **Monthly Rainfall** - Grouped bar chart by year
- **Rainfall Statistics** - Total, average, rainy days
- **Intensity Distribution** - Pie chart of rain categories

### 4️⃣ **Seasonal Patterns Tab** 🍂
- **Temperature by Season** - Grouped bar comparison
- **Box Plots** - Temperature distribution per season
- **Seasonal Statistics Table** - Comprehensive seasonal data

### 5️⃣ **Statistical Analysis Tab** 📊
- **Correlation Matrix** - Interactive heatmap
- **Temperature Categories** - Distribution bar chart
- **Summary Statistics** - Descriptive stats table

### 6️⃣ **Raw Data Tab** 📅
- **Sortable Data Table** - View and sort any column
- **Row Count Selector** - Display 10, 25, 50, 100, or 500 rows
- **CSV Export** - Download filtered data

---

## 🔄 Data Pipeline

```
┌─────────────────┐
│  Raw CSV Data   │  weather.csv (96,453 rows)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Data Loading   │  PySpark reads CSV with schema inference
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Data Cleaning   │  • Remove nulls
└────────┬────────┘  • Fill missing values
         │          • Cast data types
         │          • Remove duplicates
         ▼
┌─────────────────┐
│Feature Engineer │  • Extract date components
└────────┬────────┘  • Create Season column
         │          • Create Temp_Category
         │          • Create Rain_Category
         ▼
┌─────────────────┐
│ Save Processed  │  weather_processed.csv (4,019 rows)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Analysis      │  • Yearly trends
└────────┬────────┘  • Monthly patterns
         │          • Seasonal analysis
         │          • Correlations
         │          • Extremes
         ▼
┌─────────────────┐
│ Analysis CSVs   │  6 result files
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Dashboard     │  Interactive Streamlit app
└─────────────────┘
```

---

## 📈 Analysis Outputs

### Generated Files

| File | Description | Rows | Columns |
|------|-------------|------|---------|
| `yearly_trends.csv` | Temperature stats by year | 12 | 5 |
| `monthly_trends.csv` | Temperature stats by month | 144 | 5 |
| `seasonal_patterns.csv` | Seasonal averages | 4 | 6 |
| `rainfall_patterns.csv` | Monthly precipitation | 144 | 5 |
| `temperature_distribution.csv` | Temp category counts | 5 | 3 |
| `correlation_matrix.csv` | Variable correlations | 5 | 6 |

### Sample Insights

**Yearly Temperature Trends:**
```
Year | Avg_Temperature | Max_Temperature | Min_Temperature | Record_Count
-----|-----------------|-----------------|-----------------|-------------
2006 |          10.33  |          27.01  |         -11.22  |         365
2007 |          11.27  |          30.88  |          -7.52  |         365
2008 |          11.31  |          30.82  |         -11.02  |         366
```

**Seasonal Patterns:**
```
Season | Avg_Temperature | Avg_Humidity | Avg_Wind_Speed | Total_Precipitation
-------|-----------------|--------------|----------------|--------------------
Spring |          11.25  |         0.72 |          10.50 |             2530.0
Summer |          20.60  |         0.71 |           7.81 |             2530.0
Autumn |          10.93  |         0.81 |           8.69 |             2502.5
Winter |           1.26  |         0.86 |          11.05 |             2485.0
```

---

## 📸 Screenshots

### Dashboard Overview
![Dashboard](screenshots/dashboard_overview.png)

### Temperature Trends
![Temperature](screenshots/temperature_trends.png)

### Statistical Analysis
![Statistics](screenshots/statistical_analysis.png)

---

## 🐛 Troubleshooting

### Common Issues

#### 1. **Java Not Found Error**
```
Error: The system cannot find the path specified
```

**Solution:**
```bash
# Install Java 11
# Download from: https://adoptium.net/temurin/releases/

# Set JAVA_HOME
# Windows:
$env:JAVA_HOME = "C:\Program Files\Eclipse Adoptium\jdk-11.0.28.6-hotspot"

# Linux/Mac:
export JAVA_HOME="/usr/lib/jvm/java-11-openjdk"
```

#### 2. **PySpark Version Mismatch**
```
Error: class file version 61.0
```

**Solution:**
```bash
# Downgrade PySpark to work with Java 11
pip install pyspark==3.3.0
```

#### 3. **Module Not Found: 'distutils'**
```
ModuleNotFoundError: No module named 'distutils'
```

**Solution:**
```bash
pip install setuptools
```

#### 4. **Streamlit ScriptRunContext Warning**
```
WARNING: Thread 'MainThread': missing ScriptRunContext
```

**Solution:**
```bash
# Run with streamlit command (NOT python)
streamlit run streamlit_app_updated.py
```

#### 5. **Port Already in Use**
```
Error: Port 8501 is already in use
```

**Solution:**
```bash
# Use different port
streamlit run streamlit_app_updated.py --server.port 8502
```

---

## 🔧 Configuration

### requirements.txt
```txt
pyspark==3.3.0
pandas>=2.0.0
streamlit>=1.28.0
plotly>=5.17.0
setuptools>=68.0.0
```

### Environment Variables
```bash
# Required
JAVA_HOME=/path/to/java

# Optional (for optimization)
SPARK_HOME=/path/to/spark
HADOOP_HOME=/path/to/hadoop
```

---

## 📊 Dataset Information

### Source
Historical weather data from **NOAA** (National Oceanic and Atmospheric Administration)

### Specifications
- **Records**: 96,453 raw entries
- **Processed**: 4,019 unique daily records
- **Time Period**: 2006-2017
- **Location**: Global weather stations
- **Format**: CSV with headers

### Columns

| Column | Type | Description |
|--------|------|-------------|
| Date | Date | Observation date |
| Temperature | Float | Temperature in Celsius |
| Humidity | Float | Humidity percentage (0-1) |
| Wind_Speed | Float | Wind speed in km/h |
| Pressure | Float | Atmospheric pressure in millibars |
| Precipitation | Float | Daily precipitation in mm |
| Season | String | Calculated season (Spring/Summer/Autumn/Winter) |
| Temp_Category | String | Temperature classification |

---

## 🎓 Learning Outcomes

This project demonstrates:

1. **Big Data Processing** - Handling large datasets with PySpark
2. **ETL Pipelines** - Extract, Transform, Load workflows
3. **Data Cleaning** - Handling missing values and outliers
4. **Feature Engineering** - Creating derived columns
5. **Statistical Analysis** - Descriptive and correlation analysis
6. **Data Visualization** - Interactive charts with Plotly
7. **Web Development** - Building dashboards with Streamlit
8. **Production Code** - Error handling, logging, and documentation

---

## 🚀 Future Enhancements

- [ ] Add machine learning models for weather prediction
- [ ] Implement time series forecasting (ARIMA, Prophet)
- [ ] Add map-based visualizations for geographical data
- [ ] Integrate real-time weather API data
- [ ] Deploy to cloud (AWS, Azure, GCP)
- [ ] Add authentication and user management
- [ ] Implement caching for better performance
- [ ] Add more statistical tests and anomaly detection

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Format code
black src/
flake8 src/
```

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)
- Email: your.email@example.com

---

## 🙏 Acknowledgments

- **Apache Spark** for distributed computing framework
- **Streamlit** for amazing dashboard capabilities
- **Plotly** for interactive visualizations
- **NOAA** for providing weather data
- **Python Community** for excellent libraries and support

---

## 📚 References

- [PySpark Documentation](https://spark.apache.org/docs/latest/api/python/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Python](https://plotly.com/python/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

---

## ⭐ Star This Repository

If you found this project helpful, please consider giving it a star! ⭐

---

**Built with ❤️ using Python, PySpark, and Streamlit**

Last Updated: October 31, 2025
