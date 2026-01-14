import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Yaqeen Institute - Executive Analytics",
    page_icon="🛡️",
    layout="wide"
)

# ==========================================
# CUSTOM CSS & TAILWIND INJECTION
# ==========================================

st.markdown("""
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
    /* Custom Overrides for Streamlit Elements to match Dark Theme */
    div[data-testid="metric-container"] {
        background-color: #1e293b; /* Slate-800 */
        border: 1px solid #334155; /* Slate-700 */
        padding: 15px;
        border-radius: 8px;
        color: white;
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
    n_rows = 15000 
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 12, 31)
    
    # Dimensions
    regions = ['North America', 'MENA', 'Europe', 'SEA', 'Oceania']
    segments = ['Gen-Z', 'Millennial', 'Gen-X', 'Boomer']
    
    # Generate random dates
    date_range_days = (end_date - start_date).days
    random_days = np.random.randint(0, date_range_days + 1, n_rows)
    dates = [start_date + timedelta(days=int(day)) for day in random_days]
    
    data = {
        'date': dates,
        'user_id': [f'u{np.random.randint(1000, 9999)}' for _ in range(n_rows)],
        'region': np.random.choice(regions, n_rows, p=[0.4, 0.3, 0.15, 0.1, 0.05]), 
        'segment': np.random.choice(segments, n_rows, p=[0.35, 0.35, 0.2, 0.1]),
        'session_duration_sec': np.random.randint(30, 900, n_rows),
        # Simulated BASIC Scores
        'belief_score': np.random.randint(60, 100, n_rows),
        'attitude_score': np.random.randint(40, 90, n_rows), 
        'spiritual_score': np.random.randint(50, 95, n_rows),
        'institutional_score': np.random.randint(30, 85, n_rows), 
        'contribution_score': np.random.randint(70, 100, n_rows),
    }
    
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    
    # Derived Aggregate Score
    df['basic_aggregate'] = df[['belief_score', 'attitude_score', 'spiritual_score', 'institutional_score', 'contribution_score']].mean(axis=1)
    
    return df.sort_values('date')

# Load Data
df_master = generate_data()

# ==========================================
# 2. SIDEBAR
# ==========================================
with st.sidebar:
    st.markdown("### 👨‍💻 About this Project")
    st.info(
        "**TPM Case Study Prototype**\n"
        "Simulating 'Health of the Ummah' monitoring dashboard.\n\n"
        "📂 **Source Code:**\n"
        "[github.com/darefatir/yaqeen-dashboard](https://github.com/darefatir/yaqeen-dashboard)"
    )
    st.divider()

    st.header("🔍 Filter Dashboard")

    # Filters
    min_date = df_master['date'].min().date()
    max_date = df_master['date'].max().date()
    start_date, end_date = st.date_input("Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)

    region_list = sorted(df_master['region'].unique())
    selected_regions = st.multiselect("Select Region", region_list, default=region_list)

    segment_list = sorted(df_master['segment'].unique())
    selected_segments = st.multiselect("Select Age Segment", segment_list, default=segment_list)

    st.markdown("---")
    st.caption("💡 **Pro Tip:** Filter for *'Gen-Z'* in *'North America'* to see the Critical Drop logic.")

# ==========================================
# 3. FILTERING LOGIC
# ==========================================
if isinstance(start_date,  pd.Timestamp): start_date = start_date.date()
if isinstance(end_date, pd.Timestamp): end_date = end_date.date()

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
st.markdown(f"**Data Period:** {start_date} to {end_date} | **Active Filters:** {len(selected_regions)} Regions, {len(selected_segments)} Segments")
st.divider()

tab1, tab2 = st.tabs(["📊 Executive Overview (Interactive)", "🛠️ Data Pipeline & Architecture"])

# ------------------------------------------
# TAB 1: EXECUTIVE DASHBOARD
# ------------------------------------------
with tab1:
    # --- ROW 1: KPI CARDS WITH TARGETS ---
    st.subheader("1. Key Performance Indicators (Actual vs. Target)")
    
    # Calculate Actuals & Targets
    actual_users = df_filtered['user_id'].nunique()
    actual_sessions = len(df_filtered)
    actual_duration = df_filtered['session_duration_sec'].mean()
    actual_score = df_filtered['basic_aggregate'].mean()

    target_users = 8500 if len(df_filtered) < 5000 else 12000 
    target_sessions = 12000 if len(df_filtered) < 5000 else 18000
    target_duration = 300 
    target_score = 80.0 

    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        delta_users = ((actual_users - target_users) / target_users) * 100
        st.metric("Active Users", f"{actual_users:,.0f} / {target_users:,.0f}", f"{delta_users:.1f}% vs Target")
    with c2:
        delta_sessions = ((actual_sessions - target_sessions) / target_sessions) * 100
        st.metric("Total Sessions", f"{actual_sessions:,.0f} / {target_sessions:,.0f}", f"{delta_sessions:.1f}% vs Target")
    with c3:
        delta_duration = actual_duration - target_duration
        st.metric("Avg. Duration (sec)", f"{actual_duration:.0f}s / {target_duration}s", f"{delta_duration:.0f}s vs Target")
    with c4:
        delta_score = actual_score - target_score
        st.metric("Avg. Spiritual Health", f"{actual_score:.1f} / {target_score}", 
                  delta=f"{delta_score:.1f} vs Target", 
                  delta_color="normal" if actual_score >= target_score else "inverse")

    st.markdown("---")

    # --- ROW 2: MAIN VISUALIZATION (SPLIT VIEW) ---
    col_left, col_right = st.columns([1.2, 1.8]) 

    # === LEFT COLUMN: HEALTH METER & FORMULA ===
    with col_left:
        st.subheader("2. Benchmarking: 'Health of the Ummah'")
        
        # A. GAUGE CHART
        current_score = actual_score if not np.isnan(actual_score) else 0
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = current_score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "<b>Aggregate BASIC Score</b>", 'font': {'size': 16}},
            delta = {'reference': target_score, 'increasing': {'color': "green"}},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "#f28c28"},
                'steps': [
                    {'range': [0, 60], 'color': '#5e1b1b'},
                    {'range': [60, 80], 'color': '#d69e2e'},
                    {'range': [80, 100], 'color': '#22543d'}],
                'threshold': {'line': {'color': "white", 'width': 4}, 'thickness': 0.75, 'value': target_score}}))
        
        fig_gauge.update_layout(height=280, margin=dict(l=20, r=20, t=30, b=0))
        st.plotly_chart(fig_gauge, use_container_width=True)

        # B. FORMULA / EXPLANATION (RESTORED)
        with st.expander("ℹ️ How is this score calculated?"):
            st.markdown("""
            The **Aggregate Score** represents the holistic spiritual health of the selected segment. 
            It is calculated as the **mean** of the 5 BASIC dimensions:
            
            $$
            \\text{Score} = \\frac{B + A + S + I + C}{5}
            $$
            
            **Legend:**
            * **B** = Belief (Key Truths)
            * **A** = Attitude (Doubts/Conviction)
            * **S** = Spiritual (Worship Habits)
            * **I** = Institutional (Community/Masjid)
            * **C** = Contribution (Service/Dawah)
            """)

        # C. HORIZONTAL BARS
        st.markdown("##### BASIC Dimensions vs. Quarterly Goals")
        
        dim_scores = {
            'Dimension': ['Belief (B)', 'Attitude (A)', 'Spiritual (S)', 'Institutional (I)', 'Contribution (C)'],
            'Score': [
                df_filtered['belief_score'].mean(),
                df_filtered['attitude_score'].mean(),
                df_filtered['spiritual_score'].mean(),
                df_filtered['institutional_score'].mean(),
                df_filtered['contribution_score'].mean()
            ]
        }
        df_dims = pd.DataFrame(dim_scores)

        def get_color(score):
            if score >= 75: return '#38a169'
            elif score >= 60: return '#d69e2e'
            else: return '#e53e3e'

        df_dims['Color'] = df_dims['Score'].apply(get_color)
        df_dims['Status'] = df_dims['Score'].apply(lambda x: "✅ On Track" if x>=75 else ("⚠️ Below Target" if x>=60 else "🚨 Critical"))

        fig_bars = go.Figure()
        fig_bars.add_trace(go.Bar(
            y=df_dims['Dimension'],
            x=df_dims['Score'],
            orientation='h',
            marker=dict(color=df_dims['Color']),
            text=df_dims['Score'].apply(lambda x: f"{x:.1f}%"),
            textposition='auto',
            hovertext=df_dims['Status']
        ))

        fig_bars.update_layout(
            xaxis=dict(range=[0, 100], showgrid=True, gridcolor='#333'),
            yaxis=dict(autorange="reversed"), 
            height=300,
            margin=dict(l=0, r=0, t=10, b=0),
            showlegend=False
        )
        st.plotly_chart(fig_bars, use_container_width=True)

        # D. INSIGHT ALERT (USING TAILWIND CSS)
        if "North America" in selected_regions and "Gen-Z" in selected_segments:
             # Using Tailwind classes directly in HTML
             st.markdown("""
             <div class="bg-red-900 border-l-4 border-red-500 text-red-100 p-4 rounded shadow-lg mt-4" role="alert">
                <p class="font-bold">⚠️ Insight Alert</p>
                <p>'Institutional' score is critically low (-15% vs Avg) for this segment.</p>
             </div>
             """, unsafe_allow_html=True)

    # === RIGHT COLUMN: TRENDS ===
    with col_right:
        st.subheader("3. Trend Analysis: Engagement Over Time")
        
        daily_trend = df_filtered.set_index('date').resample('D').size().reset_index(name='sessions')
        
        fig_trend = px.area(
            daily_trend, 
            x='date', 
            y='sessions',
            title="Daily Session Volume (2025)",
            color_discrete_sequence=['#3182ce']
        )
        
        fig_trend.update_layout(
            xaxis_title="",
            yaxis_title="Total Sessions",
            height=500,
            hovermode="x unified"
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    # --- ROW 3: RAW DATA ---
    with st.expander("📂 View Filtered Source Data (Gold Layer)"):
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
