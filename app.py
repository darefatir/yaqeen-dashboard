import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Yaqeen Institute - BASIC Data Product",
    page_icon="🕌",
    layout="wide"
)

# --- CUSTOM CSS FOR STYLING ---
st.markdown("""
    <style>
    .big-font { font-size:20px !important; }
    .alert-box {
        background-color: #5e1b1b;
        color: white;
        padding: 20px;
        border-radius: 10px;
        border-left: 10px solid #ff4b4b;
        margin-bottom: 20px;
    }
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
st.title("🛡️ Yaqeen Institute: BASIC Intelligence Platform")
st.markdown("**TPM Technical Assessment Prototype** | Monitoring 'Health of the Ummah' & Data Lineage")
st.divider()

# --- TABS FOR DIFFERENT VIEWS ---
tab1, tab2 = st.tabs(["📊 Executive Dashboard (Tactical)", "🛠️ Data Pipeline (Lineage)"])

# ==========================================
# TAB 1: EXECUTIVE DASHBOARD (Slide: Tactical Insights)
# ==========================================
with tab1:
    st.subheader("Organizational Benchmarking & Tactical Response")
    
    # Layout: Split Left (Monitoring) and Right (Action)
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.info("### 📡 Benchmarking: The 'Health of the Ummah'")
        
        # 1. GAUGE CHART (Speedometer)
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = 72,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Aggregate Spiritual Health Score"},
            delta = {'reference': 70, 'increasing': {'color': "green"}},
            gauge = {
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
                'bar': {'color': "#f28c28"}, # Orange Yaqeen
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 50], 'color': '#5e1b1b'},
                    {'range': [50, 75], 'color': '#d69e2e'},
                    {'range': [75, 100], 'color': '#22543d'}],
                'threshold': {
                    'line': {'color': "white", 'width': 4},
                    'thickness': 0.75,
                    'value': 80}}))
        
        fig_gauge.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig_gauge, use_container_width=True)

        # 2. HORIZONTAL BARS (BASIC Dimensions)
        # Data preparation
        data_dims = {
            'Dimension': ['Belief (B)', 'Attitude (A)', 'Spiritual (S)', 'Institutional (I)', 'Contribution (C)'],
            'Score': [78, 65, 70, 55, 82],
            'Status': ['On Track', 'Below Target', 'Below Target', 'CRITICAL', 'Exceeds Target'],
            'Color': ['#38a169', '#d69e2e', '#d69e2e', '#e53e3e', '#38a169'] # Green, Yellow, Red
        }
        df_dims = pd.DataFrame(data_dims)

        fig_bars = px.bar(
            df_dims, 
            x='Score', 
            y='Dimension', 
            orientation='h', 
            text='Score',
            color='Status',
            color_discrete_map={
                'On Track': '#38a169', 
                'Exceeds Target': '#2f855a', 
                'Below Target': '#d69e2e', 
                'CRITICAL': '#e53e3e'
            }
        )
        fig_bars.update_layout(showlegend=False, height=250, margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig_bars, use_container_width=True)

    with col_right:
        st.warning("### ⚡ Tactical Response: Scenario Drill-Down")
        
        # 3. ALERT BOX (Simulating the Red Alert in Slide)
        st.markdown("""
        <div class="alert-box">
            <h3>⚠️ INSIGHT ALERT: CRITICAL DROP DETECTED</h3>
            <p><strong>'Institutional Connection'</strong> score dropped <strong>15%</strong> this month among <strong>Gen-Z users in North America</strong>.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### ⚙️ Automated Response Protocol")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("##### 🤖 Path 1: Automated")
            st.success("**Trigger In-App Nudge**")
            st.caption("Action: Pushed localized 'Community & Masjid' content feed to affected segment.")
            st.markdown("✅ *Status: Executed at 09:00 AM*")
            
        with c2:
            st.markdown("##### 👤 Path 2: Manual")
            st.error("**Alert Content Team**")
            st.caption("Action: Slack alert sent to schedule emergency live Q&A webinar.")
            st.markdown("⏳ *Status: Pending Approval*")

# ==========================================
# TAB 2: DATA ARCHITECTURE (Slide: Bronze-Silver-Gold)
# ==========================================
with tab2:
    st.subheader("Data Architecture: The Bronze-Silver-Gold Pipeline")
    st.caption("Traceability example: From raw user behavior to aggregated BASIC scores (Powered by dbt & Redshift).")

    # Layout: 3 Columns for 3 Layers
    col_bronze, col_arrow1, col_silver, col_arrow2, col_gold = st.columns([3, 0.5, 3, 0.5, 3])

    # --- BRONZE LAYER ---
    with col_bronze:
        st.markdown("### 🥉 1. Bronze Layer")
        st.markdown("*(Raw Ingestion - Immutable)*")
        st.code("Table: raw.tracks", language="sql")
        
        # Mock Raw Data
        bronze_data = pd.DataFrame({
            "received_at": ["2026-01-15 10:00:01", "2026-01-15 10:05:22"],
            "event_type": ["video_watched", "article_read"],
            "properties (JSON)": [
                '{"user_id": "u123", "vid_id": "vid_doubt_01", "pct": 0.5}',
                '{"user_id": "u124", "art_id": "art_belief_99", "scroll": 0.9}'
            ]
        })
        st.dataframe(bronze_data, hide_index=True, use_container_width=True)

    with col_arrow1:
        st.markdown("<br><br><br>➡️<br>dbt<br>Clean", unsafe_allow_html=True)

    # --- SILVER LAYER ---
    with col_silver:
        st.markdown("### 🥈 2. Silver Layer")
        st.markdown("*(Enriched & Staged)*")
        st.code("Table: stg.video_events + dim.content", language="sql")
        
        # Mock Silver Data
        silver_data = pd.DataFrame({
            "user_id": ["u123", "u124"],
            "content_id": ["vid_doubt_01", "art_belief_99"],
            "BASIC_tag": ["Attitude", "Belief"],
            "weight": [-3.0, 5.0]
        })
        st.dataframe(silver_data, hide_index=True, use_container_width=True)
        st.caption("Joined with AI-generated metadata tags.")

    with col_arrow2:
        st.markdown("<br><br><br>➡️<br>dbt<br>Agg", unsafe_allow_html=True)

    # --- GOLD LAYER ---
    with col_gold:
        st.markdown("### 🥇 3. Gold Layer")
        st.markdown("*(Serving Mart - Business Ready)*")
        st.code("Table: mart.fact_basic_daily", language="sql")
        
        # Mock Gold Data
        gold_data = pd.DataFrame({
            "date_key": ["2026-01-15", "2026-01-15"],
            "user_key": ["u123", "u124"],
            "attitude_score": [65.5, 70.0],
            "belief_score": [80.0, 85.0]
        })
        st.dataframe(gold_data, hide_index=True, use_container_width=True)
        st.caption("Final scores ready for Dashboard/API.")

# ==========================================
# RAW DATA SECTION (Bottom)
# ==========================================
st.divider()
st.subheader("📂 Source Data (Mart Layer Preview)")
st.markdown("This section displays the raw underlying data from `mart.fact_basic_daily` used to power the dashboards above.")

# Generate Dummy Big Data for Display
df_raw = pd.DataFrame({
    'date': pd.date_range(start='2026-01-01', periods=10).repeat(5),
    'user_id': [f'u{i}' for i in range(100, 150)],
    'segment': ['Gen-Z', 'Millennial', 'Gen-X', 'Boomer', 'Gen-Z'] * 10,
    'region': ['North America', 'MENA', 'Europe', 'SEA', 'North America'] * 10,
    'belief_score': [78, 80, 85, 90, 75] * 10,
    'attitude_score': [65, 70, 72, 60, 55] * 10, # Note the 55 for GenZ/NA to match scenario
    'institutional_score': [55, 60, 80, 85, 52] * 10,
    'action_trigger': ['Automated Nudge', 'None', 'None', 'None', 'Manual Alert'] * 10
})

st.dataframe(df_raw, use_container_width=True, height=300)
