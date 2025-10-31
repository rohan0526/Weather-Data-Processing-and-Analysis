"""
Streamlit Weather Dashboard - Fixed Version
Interactive visualization of weather analysis results
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Page configuration
st.set_page_config(
    page_title="Weather Analysis Dashboard",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    </style>
    """, unsafe_allow_html=True)


@st.cache_data
def load_processed_data():
    """Load processed weather data"""
    try:
        root = os.path.dirname(os.path.abspath(__file__))
        df = pd.read_csv(os.path.join(root, "data", "weather_processed.csv"))
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    except FileNotFoundError:
        st.error("❌ Processed data not found. Please run data_processor.py first.")
        return None


@st.cache_data
def load_analysis_results():
    """Load pre-computed analysis results"""
    results = {}
    root = os.path.dirname(os.path.abspath(__file__))
    result_dir = os.path.join(root, "data", "analysis_results")
    
    if not os.path.exists(result_dir):
        return results
    
    files = {
        'yearly': 'yearly_trends.csv',
        'monthly': 'monthly_trends.csv',
        'seasonal': 'seasonal_patterns.csv',
        'rainfall': 'rainfall_patterns.csv',
        'temp_dist': 'temperature_distribution.csv'
    }
    
    for key, filename in files.items():
        filepath = os.path.join(result_dir, filename)
        if os.path.exists(filepath):
            results[key] = pd.read_csv(filepath)
    
    return results


def main():
    """Main dashboard function"""
    
    # Header
    st.title("🌤️ Weather Data Analysis Dashboard")
    st.markdown("---")
    
    # Load data
    df = load_processed_data()
    
    if df is None:
        st.stop()
    
    analysis_results = load_analysis_results()
    
    # Sidebar filters
    st.sidebar.header("📊 Filters")
    
    # Year filter
    years = sorted(df['Year'].unique())
    selected_years = st.sidebar.multiselect(
        "Select Years",
        options=years,
        default=years
    )
    
    # Season filter
    seasons = sorted(df['Season'].unique())
    selected_seasons = st.sidebar.multiselect(
        "Select Seasons",
        options=seasons,
        default=seasons
    )
    
    # Filter dataframe
    df_filtered = df[
        (df['Year'].isin(selected_years)) & 
        (df['Season'].isin(selected_seasons))
    ]
    
    # Key Metrics
    st.header("📈 Key Statistics")
    
    # Calculate metrics
    avg_temp = df_filtered['Temperature'].mean() if len(df_filtered) > 0 else 0
    max_temp = df_filtered['Temperature'].max() if len(df_filtered) > 0 else 0
    min_temp = df_filtered['Temperature'].min() if len(df_filtered) > 0 else 0
    total_records = len(df_filtered)
    
    # Display metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Average Temperature", f"{avg_temp:.2f}°C", delta=None)
    
    with col2:
        st.metric("Maximum Temperature", f"{max_temp:.2f}°C", delta=None)
    
    with col3:
        st.metric("Minimum Temperature", f"{min_temp:.2f}°C", delta=None)
    
    with col4:
        st.metric("Total Records", f"{total_records:,}", delta=None)
    
    st.markdown("---")
    
    # Visualization tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🌡️ Temperature Trends", 
        "🌧️ Rainfall Analysis", 
        "🍂 Seasonal Patterns",
        "📊 Statistical Analysis",
        "📅 Raw Data"
    ])
    
    # Tab 1: Temperature Trends
    with tab1:
        st.subheader("Temperature Trends Over Time")
        
        # Time series plot
        fig_temp = px.line(
            df_filtered,
            x='Date',
            y='Temperature',
            title='Daily Temperature Variation',
            labels={'Temperature': 'Temperature (°C)', 'Date': 'Date'},
            color_discrete_sequence=['#FF6B6B']
        )
        fig_temp.update_layout(height=400)
        st.plotly_chart(fig_temp, use_container_width=True)
        
        # Yearly trends
        if 'yearly' in analysis_results:
            yearly_df = analysis_results['yearly']
            yearly_df = yearly_df[yearly_df['Year'].isin(selected_years)]
            
            fig_yearly = go.Figure()
            fig_yearly.add_trace(go.Scatter(
                x=yearly_df['Year'],
                y=yearly_df['Avg_Temperature'],
                mode='lines+markers',
                name='Average',
                line=dict(color='#4ECDC4', width=3)
            ))
            fig_yearly.add_trace(go.Scatter(
                x=yearly_df['Year'],
                y=yearly_df['Max_Temperature'],
                mode='lines+markers',
                name='Maximum',
                line=dict(color='#FF6B6B', dash='dash')
            ))
            fig_yearly.add_trace(go.Scatter(
                x=yearly_df['Year'],
                y=yearly_df['Min_Temperature'],
                mode='lines+markers',
                name='Minimum',
                line=dict(color='#95E1D3', dash='dash')
            ))
            
            fig_yearly.update_layout(
                title='Yearly Temperature Trends',
                xaxis_title='Year',
                yaxis_title='Temperature (°C)',
                height=400
            )
            st.plotly_chart(fig_yearly, use_container_width=True)
        
        # Monthly heatmap
        col1, col2 = st.columns(2)
        
        with col1:
            monthly_avg = df_filtered.groupby(['Year', 'Month'])['Temperature'].mean().reset_index()
            if len(monthly_avg) > 0:
                try:
                    pivot_temp = monthly_avg.pivot(index='Month', columns='Year', values='Temperature')
                    
                    fig_heatmap = px.imshow(
                    pivot_temp,
                    labels=dict(x="Year", y="Month", color="Temperature (°C)"),
                    title="Monthly Temperature Heatmap",
                    color_continuous_scale='RdYlBu_r',
                    aspect='auto'
                )
                    fig_heatmap.update_layout(height=400)
                    st.plotly_chart(fig_heatmap, use_container_width=True)
                except Exception as e:
                    st.info("Not enough data for heatmap visualization.")
        
        with col2:
            # Temperature distribution
            fig_hist = px.histogram(
                df_filtered,
                x='Temperature',
                nbins=50,
                title='Temperature Distribution',
                labels={'Temperature': 'Temperature (°C)', 'count': 'Frequency'},
                color_discrete_sequence=['#4ECDC4']
            )
            fig_hist.update_layout(height=400)
            st.plotly_chart(fig_hist, use_container_width=True)
    
    # Tab 2: Rainfall Analysis
    with tab2:
        st.subheader("Rainfall Patterns")
        
        if 'Precipitation' in df_filtered.columns:
            # Monthly rainfall
            monthly_rain = df_filtered.groupby(['Year', 'Month'])['Precipitation'].sum().reset_index()
            
            if len(monthly_rain) > 0:
                try:
                    fig_rain = px.bar(
                        monthly_rain,
                        x='Month',
                        y='Precipitation',
                        color='Year',
                        title='Monthly Rainfall by Year',
                        labels={'Precipitation': 'Precipitation (mm)', 'Month': 'Month'},
                        barmode='group'
                    )
                    fig_rain.update_layout(height=400)
                    st.plotly_chart(fig_rain, use_container_width=True)
                except Exception as e:
                    st.info("Not enough data for rainfall visualization.")
            
            # Rainfall statistics
            col1, col2 = st.columns(2)
            
            with col1:
                total_rain = df_filtered['Precipitation'].sum()
                avg_rain = df_filtered['Precipitation'].mean()
                rainy_days = len(df_filtered[df_filtered['Precipitation'] > 0])
                
                st.metric("Total Precipitation", f"{total_rain:.2f} mm")
                st.metric("Average Daily Precipitation", f"{avg_rain:.2f} mm")
                st.metric("Rainy Days", rainy_days)
        else:
            st.info("Precipitation data not available in the dataset.")
    
    # Tab 3: Seasonal Patterns
    with tab3:
        st.subheader("Seasonal Weather Patterns")
        
        # Seasonal temperature comparison
        seasonal_temp = df_filtered.groupby('Season').agg({
            'Temperature': ['mean', 'min', 'max'],
            'Humidity': 'mean',
            'Wind_Speed': 'mean'
        }).reset_index()
        seasonal_temp.columns = ['Season', 'Avg_Temp', 'Min_Temp', 'Max_Temp', 'Avg_Humidity', 'Avg_Wind_Speed']
        
        if len(seasonal_temp) > 0:
            # Temperature by season
            fig_season_temp = go.Figure()
            fig_season_temp.add_trace(go.Bar(
                x=seasonal_temp['Season'],
                y=seasonal_temp['Avg_Temp'],
                name='Average',
                marker_color='#4ECDC4'
            ))
            fig_season_temp.add_trace(go.Bar(
                x=seasonal_temp['Season'],
                y=seasonal_temp['Max_Temp'],
                name='Maximum',
                marker_color='#FF6B6B'
            ))
            fig_season_temp.add_trace(go.Bar(
                x=seasonal_temp['Season'],
                y=seasonal_temp['Min_Temp'],
                name='Minimum',
                marker_color='#95E1D3'
            ))
            
            fig_season_temp.update_layout(
                title='Temperature by Season',
                xaxis_title='Season',
                yaxis_title='Temperature (°C)',
                barmode='group',
                height=400
            )
            st.plotly_chart(fig_season_temp, use_container_width=True)
            
            # Box plot for temperature distribution by season
            fig_box = px.box(
                df_filtered,
                x='Season',
                y='Temperature',
                title='Temperature Distribution by Season',
                color='Season'
            )
            fig_box.update_layout(height=400)
            st.plotly_chart(fig_box, use_container_width=True)
            
            # Seasonal statistics table
            st.dataframe(seasonal_temp.style.format({
                'Avg_Temp': '{:.2f}',
                'Min_Temp': '{:.2f}',
                'Max_Temp': '{:.2f}',
                'Avg_Humidity': '{:.2f}',
                'Avg_Wind_Speed': '{:.2f}'
            }), use_container_width=True)
    
    # Tab 4: Statistical Analysis
    with tab4:
        st.subheader("Statistical Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Correlation heatmap
            numeric_cols = ['Temperature', 'Humidity', 'Wind_Speed', 'Precipitation', 'Pressure']
            available_cols = [col for col in numeric_cols if col in df_filtered.columns]
            
            if len(available_cols) > 1:
                corr_matrix = df_filtered[available_cols].corr()
                
                fig_corr = px.imshow(
                    corr_matrix,
                    labels=dict(color="Correlation"),
                    title="Correlation Matrix",
                    color_continuous_scale='RdBu_r',
                    aspect='auto',
                    text_auto='.2f'
                )
                fig_corr.update_layout(height=400)
                st.plotly_chart(fig_corr, use_container_width=True)
        
        with col2:
            # Temperature category distribution
            if 'Temp_Category' in df_filtered.columns:
                temp_cat = df_filtered['Temp_Category'].value_counts()
                fig_temp_cat = px.bar(
                    x=temp_cat.index,
                    y=temp_cat.values,
                    title='Temperature Category Distribution',
                    labels={'x': 'Category', 'y': 'Count'},
                    color=temp_cat.values,
                    color_continuous_scale='RdYlBu_r'
                )
                fig_temp_cat.update_layout(height=400)
                st.plotly_chart(fig_temp_cat, use_container_width=True)
        
        # Summary statistics
        st.subheader("Summary Statistics")
        st.dataframe(df_filtered[available_cols].describe(), use_container_width=True)
    
    # Tab 5: Raw Data
    with tab5:
        st.subheader("Raw Data")
        
        # Display options
        col1, col2 = st.columns(2)
        with col1:
            num_rows = st.selectbox("Number of rows to display", [10, 25, 50, 100, 500])
        with col2:
            if len(df_filtered.columns) > 0:
                sort_by = st.selectbox("Sort by", df_filtered.columns)
            else:
                sort_by = None
        
        # Display data
        if sort_by and len(df_filtered) > 0:
            st.dataframe(
                df_filtered.sort_values(by=sort_by, ascending=False).head(num_rows),
                use_container_width=True
            )
        elif len(df_filtered) > 0:
            st.dataframe(df_filtered.head(num_rows), use_container_width=True)
        
        # Download button
        if len(df_filtered) > 0:
            csv = df_filtered.to_csv(index=False)
            st.download_button(
                label="📥 Download Filtered Data as CSV",
                data=csv,
                file_name="weather_data_filtered.csv",
                mime="text/csv"
            )
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: gray;'>"
        "🌤️ Weather Analysis Dashboard | Built with PySpark & Streamlit"
        "</p>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()