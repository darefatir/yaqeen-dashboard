import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Yaqeen Institute - BASIC Analytics",
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
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.title("🛡️ Yaqeen Institute: Executive Analytics Dashboard")
st.markdown("**Real-time monitoring of Ummah's Spiritual Health & Platform Growth**")
st.divider()

# --- TABS ---
tab1, tab2 = st.tabs(["📊 Executive Overview", "🛠️ Data Pipeline (Traceability)"])

# ==========================================
# TAB 1: EXECUTIVE DASHBOARD (REVISED)
# ==========================================
with tab1:
    # --- ROW 1: TOP LEVEL METRICS (Standard Web BI) ---
    st.subheader("1. Platform Growth & Engagement")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="Total Registered Users", value="124,592", delta="1.2%")
    with col2:
        st.metric(label="Monthly Active Users (MAU)", value="45,200", delta="-0.5%")
    with col3:
        st.metric(label="Total Sessions (This Month)", value="189,340", delta="5.4%")
    with col4:
        st.metric(label="Avg. Session Duration", value="4m 12s", delta="12s")

    st.markdown("---")

    # --- ROW 2: SPLIT VIEW (Spiritual Health vs Traffic Trends) ---
    col_left, col_right = st.columns([1, 2])

    # LEFT COLUMN: THE NORTH STAR (Spiritual Health)
    with col_left:
        st.subheader("2. North Star: Spiritual Health")
        
        # GAUGE CHART (Keep this as the anchor)
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = 72,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Aggregate BASIC Score"},
            delta = {'reference': 70, 'increasing': {'color': "green"}},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "#f28c28"}, # Orange Yaqeen
                'steps': [
                    {'range': [0, 50], 'color': '#5e1b1b'},
                    {'range': [50, 75], 'color': '#d69e2e'},
                    {'range': [75, 100], 'color': '#22543d'}],
                'threshold': {'line': {'color': "white", 'width': 4}, 'thickness': 0.75, 'value': 80}}))
        
        fig_gauge.update_layout(height=350, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig_gauge, use_container_width=True)

    # RIGHT COLUMN: TRAFFIC & COMPARISON
    with col_right:
        st.subheader("3. Trends & Score Comparison")
        
        # TAB WITHIN TAB for different charts
        chart_tab1, chart_tab2 = st.tabs(["📈 Traffic Trend", "bar_chart BASIC Score Breakdown"])
        
        with chart_tab1:
            # Fake Time Series Data
            dates = pd.date_range(start="2026-01-01", periods=30)
            traffic_data = pd.DataFrame({
                "Date": dates,
                "Sessions": np.random.randint(4000, 6000, size=30) + np.linspace(0, 1000, 30)
            })
            
            fig_line = px.area(traffic_data, x="Date", y="Sessions", title="Daily Session Trend (Last 30 Days)", color_discrete_sequence=['#3182ce'])
            fig_line.update_layout(height=300, xaxis_title="", yaxis_title="Sessions")
            st.plotly_chart(fig_line, use_container_width=True)
            
        with chart_tab2:
            # Comparison Data (Current vs Previous Month)
            comp_data = pd.DataFrame({
                "Dimension": ['Belief', 'Attitude', 'Spiritual', 'Institutional', 'Contribution'] * 2,
                "Score": [78, 65, 70, 55, 82, 76, 62, 68, 65, 80],
                "Period": ['Current Month'] * 5 + ['Last Month'] * 5
            })
            
            fig_bar = px.bar(comp_data, x="Dimension", y="Score", color="Period", barmode="group",
                             title="BASIC Score Comparison (MoM)",
                             color_discrete_map={'Current Month': '#f28c28', 'Last Month': '#718096'})
            fig_bar.update_layout(height=300, yaxis=dict(range=[0, 100]))
            st.plotly_chart(fig_bar, use_container_width=True)

    # --- ROW 3: INSIGHT ALERTS (Simplified List, not backend config) ---
    st.subheader("4. Key Insights & Anomalies")
    st.info("⚠️ **Critical Insight:** 'Institutional Connection' score dropped **15%** among **Gen-Z (North America)** vs Last Month. (Automated Nudge Triggered)")


# ==========================================
# TAB 2: DATA ARCHITECTURE (Keep as is - Technical Validation)
# ==========================================
with tab2:
    st.subheader("Data Architecture: The Bronze-Silver-Gold Pipeline")
    st.caption("Traceability example: From raw user behavior to aggregated BASIC scores (Powered by dbt & Redshift).")

    col_bronze, col_arrow1, col_silver, col_arrow2, col_gold = st.columns([3, 0.5, 3, 0.5, 3])

    # --- BRONZE LAYER ---
    with col_bronze:
        st.markdown("### 🥉 Bronze (Raw)")
        st.code("Table: raw.tracks", language="sql")
        bronze_data = pd.DataFrame({
            "received_at": ["2026-01-15 10:00:01", "2026-01-15 10:05:22"],
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
        gold_data = pd.DataFrame({
            "date": ["2026-01-15", "2026-01-15"],
            "user": ["u123", "u124"],
            "attitude_score": [65.5, 70.0],
            "belief_score": [80.0, 85.0]
        })
        st.dataframe(gold_data, hide_index=True, use_container_width=True)

# ==========================================
# RAW DATA SECTION
# ==========================================
st.divider()
st.subheader("📂 Raw Data Explorer (Gold Layer)")
st.markdown("Direct view of the `mart.fact_basic_daily` table for analysts.")

df_raw = pd.DataFrame({
    'date': pd.date_range(start='2026-01-01', periods=10).repeat(5),
    'user_id': [f'u{i}' for i in range(100, 150)],
    'segment': ['Gen-Z', 'Millennial', 'Gen-X', 'Boomer', 'Gen-Z'] * 10,
    'region': ['North America', 'MENA', 'Europe', 'SEA', 'North America'] * 10,
    'belief_score': [78, 80, 85, 90, 75] * 10,
    'attitude_score': [65, 70, 72, 60, 55] * 10,
    'institutional_score': [55, 60, 80, 85, 52] * 10,
})

st.dataframe(df_raw, use_container_width=True, height=300)
