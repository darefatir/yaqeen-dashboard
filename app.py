import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Yaqeen Institute - Executive Analytics",
    page_icon="🕌",
    layout="wide"
)

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .metric-card {
        background-color: #0e1117;
        border: 1px solid #30333d;
        border-radius: 5px;
        padding: 15px;
        text-align: center;
    }
    .st-emotion-cache-16txtl3 {
        padding-top: 2rem; 
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 1. DATA GENERATION ENGINE (FULL YEAR 2025)
# ==========================================
@st.cache_data
def generate_data():
    """Generates a comprehensive mock dataset for Jan 1 2025 - Dec 31 2025."""
    # Settings
    n_rows = 15000 # Increased rows to make the full year look populated
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 12, 31)
    
    # Dimensions
    regions = ['North America', 'MENA', 'Europe', 'SEA', 'Oceania']
    segments = ['Gen-Z', 'Millennial', 'Gen-X', 'Boomer']
    
    # Generate random dates within the 2025 range
    date_range_days = (end_date - start_date).days
    random_days = np.random.randint(0, date_range_days + 1, n_rows)
    dates = [start_date + timedelta(days=int(day)) for day in random_days]
    
    data = {
        'date': dates,
        'user_id': [f'u{np.random.randint(1000, 9999)}' for _ in range(n_rows)],
        'region': np.random.choice(regions, n_rows, p=[0.4, 0.3, 0.15, 0.1, 0.05]), # NA & MENA dominant
        'segment': np.random.choice(segments, n_rows, p=[0.35, 0.35, 0.2, 0.1]),
        'session_duration_sec': np.random.randint(30, 900, n_rows),
        # Simulated BASIC Scores (Random but weighted)
        'belief_score': np.random.randint(60, 100, n_rows),
        'attitude_score': np.random.randint(40, 90, n_rows), # Slightly lower (Doubt)
        'spiritual_score': np.random.randint(50, 95, n_rows),
        'institutional_score': np.random.randint(30, 85, n_rows), # Lowest (Critical)
        'contribution_score': np.random.randint(70, 100, n_rows),
    }
    
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    
    # Add a derived column for aggregate score
    df['basic_aggregate'] = df[['belief_score', 'attitude_score', 'spiritual_score', 'institutional_score', 'contribution_score']].mean(axis=1)
    
    return df.sort_values('date')

# Load Data
df_master = generate_data()

# ==========================================
# 2. SIDEBAR FILTERS
# ==========================================
st.sidebar.header("🔍 Filter Dashboard")

# A. Date Filter
min_date = df_master['date'].min().date()
max_date = df_master['date'].max().date()

start_date, end_date = st.sidebar.date_input(
    "Select Date Range",
    [min_date, max_date], # Default to Full Year
    min_value=min_date,
    max_value=max_date
)

# B. Region Filter
region_list = sorted(df_master['region'].unique())
selected_regions = st.sidebar.multiselect(
    "Select Region",
    region_list,
    default=region_list # Default select all
)

# C. Segment Filter
segment_list = sorted(df_master['segment'].unique())
selected_segments = st.sidebar.multiselect(
    "Select Age Segment",
    segment_list,
    default=segment_list
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Pro Tip:** Try filtering for *'Gen-Z'* in *'North America'* to see the Institutional Score drop.")

# ==========================================
# 3. FILTERING LOGIC
# ==========================================
# Ensure date inputs are valid before filtering
if isinstance(start_date,  pd.Timestamp):
    start_date = start_date.date()
if isinstance(end_date, pd.Timestamp):
    end_date = end_date.date()

# Filter the master dataframe based on inputs
mask = (
    (df_master['date'].dt.date >= start_date) &
    (df_master['date'].dt.date <= end_date) &
    (df_master['region'].isin(selected_regions)) &
    (df_master['segment'].isin(selected_segments))
)
df_filtered = df_master.loc[mask]

# ==========================================
# 4. DASHBOARD LAYOUT
# ==========================================
st.title("🛡️ Yaqeen Institute: Executive Analytics Dashboard")
st.markdown(f"**Data Period:** {start_date} to {end_date} (Full Year 2025) | **Records Analyzed:** {len(df_filtered):,}")
st.divider()

# --- TAB SELECTION ---
tab1, tab2 = st.tabs(["📊 Executive Overview (Interactive)", "🛠️ Data Pipeline & Architecture"])

# ------------------------------------------
# TAB 1: EXECUTIVE DASHBOARD
# ------------------------------------------
with tab1:
    # --- ROW 1: DYNAMIC KPI CARDS ---
    st.subheader("1. Key Performance Indicators (Filtered)")
    
    # Calculate Metrics dynamically from df_filtered
    total_users = df_filtered['user_id'].nunique()
    total_sessions = len(df_filtered)
    avg_duration = df_filtered['session_duration_sec'].mean()
    avg_score = df_filtered['basic_aggregate'].mean()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Active Users", f"{total_users:,.0f}")
    c2.metric("Total Sessions", f"{total_sessions:,.0f}")
    c3.metric("Avg. Session Duration", f"{avg_duration/60:.1f} min")
    c4.metric("Avg. Spiritual Health", f"{avg_score:.1f} / 100", 
              delta="-1.2" if avg_score < 75 else "+0.5", 
              delta_color="normal" if avg_score >= 75 else "inverse")

    st.markdown("---")

    # --- ROW 2: CHARTS ---
    col_left, col_right = st.columns([1, 2])

    # LEFT: GAUGE CHART (Aggregated Score)
    with col_left:
        st.subheader("2. Spiritual Health Meter")
        
        current_score = avg_score if not np.isnan(avg_score) else 0
        
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = current_score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Aggregate BASIC Score"},
            delta = {'reference': 75, 'increasing': {'color': "green"}},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "#f28c28"},
                'steps': [
                    {'range': [0, 60], 'color': '#5e1b1b'},
                    {'range': [60, 80], 'color': '#d69e2e'},
                    {'range': [80, 100], 'color': '#22543d'}],
                'threshold': {'line': {'color': "white", 'width': 4}, 'thickness': 0.75, 'value': 80}}))
        
        fig_gauge.update_layout(height=350, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig_gauge, use_container_width=True)
        
        # Insight based on filter
        if "North America" in selected_regions and "Gen-Z" in selected_segments:
             st.error("⚠️ **Alert:** Gen-Z in North America shows significantly lower 'Institutional' scores.")

    # RIGHT: TRENDS & BREAKDOWN
    with col_right:
        st.subheader("3. Trends & Dimensions Analysis")
        
        chart_type = st.radio("Select View:", ["Daily Traffic Trend", "BASIC Dimension Breakdown"], horizontal=True)
        
        if chart_type == "Daily Traffic Trend":
            # Group by date for line chart (Resample to Daily to ensure smooth line)
            daily_trend = df_filtered.set_index('date').resample('D').size().reset_index(name='sessions')
            
            fig_line = px.area(daily_trend, x='date', y='sessions', 
                               title="Daily Engagement Volume (2025)", color_discrete_sequence=['#3182ce'])
            st.plotly_chart(fig_line, use_container_width=True)
            
        else:
            # Calculate average for each dimension
            dim_avg = df_filtered[['belief_score', 'attitude_score', 'spiritual_score', 'institutional_score', 'contribution_score']].mean().reset_index()
            dim_avg.columns = ['Dimension', 'Score']
            
            # Color logic
            dim_avg['Color'] = dim_avg['Score'].apply(lambda x: '#e53e3e' if x < 60 else ('#d69e2e' if x < 75 else '#38a169'))
            
            fig_bar = px.bar(dim_avg, x='Score', y='Dimension', orientation='h', 
                             title="Average Score by Dimension (Filtered)", text_auto='.1f',
                             color='Color', color_discrete_map="identity")
            fig_bar.update_layout(xaxis=dict(range=[0, 100]))
            st.plotly_chart(fig_bar, use_container_width=True)

    # --- ROW 3: RAW DATA ---
    st.subheader("4. Granular Data View")
    with st.expander("📂 View Filtered Raw Data Records"):
        st.dataframe(df_filtered.head(100), use_container_width=True)

# ------------------------------------------
# TAB 2: DATA ARCHITECTURE (Technical)
# ------------------------------------------
with tab2:
    st.subheader("Data Architecture: The Bronze-Silver-Gold Pipeline")
    st.caption("How data flows from user action to the dashboard you see in Tab 1.")

    col_bronze, col_arrow1, col_silver, col_arrow2, col_gold = st.columns([3, 0.5, 3, 0.5, 3])

    # --- BRONZE LAYER ---
    with col_bronze:
        st.markdown("### 🥉 Bronze (Raw)")
        st.code("Table: raw.tracks", language="sql")
        bronze_data = pd.DataFrame({
            "received_at": ["2025-01-15 10:00:01", "2025-01-15 10:05:22"],
            "event_type": ["video_watched", "article_read"],
            "properties": ['{"uid": "u123", "pct": 0.5}', '{"uid": "u124", "scroll": 0.9}']
        })
        st.dataframe(bronze_data, hide_index=True, use_container_width=True)

    with col_arrow1:
        st.markdown("<br><br>➡️", unsafe_allow_html=True)

    # --- SILVER LAYER ---
    with col_silver:
        st.markdown("### 🥈 Silver (Enriched)")
        st.code("Table: stg.video_events", language="sql")
        silver_data = pd.DataFrame({
            "user_id": ["u123", "u124"],
            "BASIC_tag": ["Attitude", "Belief"],
            "weight": [-3.0, 5.0]
        })
        st.dataframe(silver_data, hide_index=True, use_container_width=True)

    with col_arrow2:
        st.markdown("<br><br>➡️", unsafe_allow_html=True)

    # --- GOLD LAYER ---
    with col_gold:
        st.markdown("### 🥇 Gold (Mart)")
        st.code("Table: mart.fact_basic_daily", language="sql")
        st.caption("Source for the Dashboard in Tab 1")
        st.dataframe(df_filtered[['date', 'user_id', 'region', 'basic_aggregate']].head(5), hide_index=True, use_container_width=True)
