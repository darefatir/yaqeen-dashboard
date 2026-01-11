import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Yaqeen BASIC Insights Engine",
    page_icon="🧭",
    layout="wide"
)

# --- 1. DATA GENERATION ENGINE (DUMMY) ---
@st.cache_data
def generate_data(n=1000):
    np.random.seed(42) # Agar data konsisten
    
    data = {
        'User_ID': [f'U-{i:04d}' for i in range(n)],
        'Age_Group': np.random.choice(['Gen Z (15-25)', 'Millennial (26-41)', 'Gen X (42-57)', 'Boomer (58+)'], n, p=[0.4, 0.35, 0.15, 0.1]),
        'Region': np.random.choice(['North America', 'Europe', 'MENA', 'Asia Pacific'], n, p=[0.5, 0.2, 0.15, 0.15]),
        'Belief_Score': np.random.normal(75, 15, n).clip(0, 100),
        'Attitude_Score': np.random.normal(70, 18, n).clip(0, 100),
        'Spiritual_Score': np.random.normal(65, 20, n).clip(0, 100),
        'Institutional_Score': np.random.normal(60, 22, n).clip(0, 100),
        'Contribution_Score': np.random.normal(55, 25, n).clip(0, 100),
        'Last_Active_Days_Ago': np.random.randint(0, 60, n)
    }
    
    df = pd.DataFrame(data)
    
    # Logic tambahan: Gen Z biasanya Institutional Score-nya lebih rendah (skenario realistis)
    df.loc[df['Age_Group'] == 'Gen Z (15-25)', 'Institutional_Score'] -= 10
    df['Institutional_Score'] = df['Institutional_Score'].clip(0, 100)
    
    # Calculate Average BASIC Score
    df['Avg_BASIC'] = df[['Belief_Score', 'Attitude_Score', 'Spiritual_Score', 'Institutional_Score', 'Contribution_Score']].mean(axis=1)
    
    return df

df = generate_data(1500)

# --- 2. SIDEBAR CONTROLS ---
st.sidebar.image("https://yaqeeninstitute.org/images/logo.svg", width=150) # Logo Yaqeen (External Link)
st.sidebar.header("🎯 Segmentation Filters")

selected_region = st.sidebar.multiselect("Select Region", options=df['Region'].unique(), default=df['Region'].unique())
selected_age = st.sidebar.multiselect("Select Age Group", options=df['Age_Group'].unique(), default=df['Age_Group'].unique())

# Filter Data
filtered_df = df[
    (df['Region'].isin(selected_region)) & 
    (df['Age_Group'].isin(selected_age))
]

st.sidebar.markdown("---")
st.sidebar.header("⚙️ Simulation Lab")
st.sidebar.caption("Product Manager Tool: Simulate the impact of strategic interventions.")
sim_lift = st.sidebar.slider("Projected Impact: Increase Institutional Connection by", 0, 20, 0, format="%d%%")

# Apply Simulation Logic
display_df = filtered_df.copy()
if sim_lift > 0:
    display_df['Institutional_Score'] = display_df['Institutional_Score'] + (display_df['Institutional_Score'] * (sim_lift/100))
    display_df['Institutional_Score'] = display_df['Institutional_Score'].clip(0, 100)
    st.sidebar.success(f"Simulation Active: +{sim_lift}% Lift applied!")

# --- 3. MAIN DASHBOARD UI ---

st.title("🧭 BASIC Insights Engine: Operational Dashboard")
st.markdown("""
> **Objective:** Real-time monitoring of the Ummah's spiritual health and identification of strategic intervention points.
""")

# A. TOP LEVEL METRICS (KPIs)
avg_scores = display_df[['Belief_Score', 'Attitude_Score', 'Spiritual_Score', 'Institutional_Score', 'Contribution_Score']].mean()

col1, col2, col3, col4, col5 = st.columns(5)
metrics = [
    ("Belief (B)", 'Belief_Score'),
    ("Attitude (A)", 'Attitude_Score'),
    ("Spiritual (S)", 'Spiritual_Score'),
    ("Institutional (I)", 'Institutional_Score'),
    ("Contribution (C)", 'Contribution_Score')
]

for col, (label, col_name) in zip([col1, col2, col3, col4, col5], metrics):
    val = display_df[col_name].mean()
    delta = None
    if sim_lift > 0 and col_name == 'Institutional_Score':
        original_val = filtered_df[col_name].mean()
        delta = f"{val - original_val:.1f} pts"
    col.metric(label, f"{val:.1f}", delta=delta)

st.markdown("---")

# B. RADAR CHART & SEGMENTATION
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("📊 The BASIC Radar")
    st.caption("Aggregate profile of the selected segment.")
    
    # Prepare data for Radar Chart
    categories = ['Belief', 'Attitude', 'Spiritual', 'Institutional', 'Contribution']
    values = avg_scores.values.tolist()
    
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Current Segment',
        line_color='#1F77B4'
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False,
        height=400
    )
    st.plotly_chart(fig_radar, use_container_width=True)

with col_right:
    st.subheader("🌍 Regional Deep Dive")
    st.caption("Comparing 'Institutional Connection' across regions (Key weakness area).")
    
    fig_bar = px.bar(
        display_df.groupby('Region')['Institutional_Score'].mean().reset_index(),
        x='Region',
        y='Institutional_Score',
        color='Institutional_Score',
        color_continuous_scale='OrRd',
        range_y=[0, 100],
        text_auto='.1f'
    )
    fig_bar.update_layout(height=400)
    st.plotly_chart(fig_bar, use_container_width=True)

# C. TACTICAL RESPONSE (Risk Analysis)
st.markdown("---")
st.subheader("🚨 Tactical Response: At-Risk Segments")
st.caption("Users with **High Doubts** (Low Attitude) but **High Influence** potential (High Contribution). These need immediate content intervention.")

# Logic: High Contribution (>70) but Low Attitude (<50)
risk_df = display_df[
    (display_df['Attitude_Score'] < 50) & 
    (display_df['Contribution_Score'] > 70)
].sort_values('Attitude_Score')

st.dataframe(
    risk_df[['User_ID', 'Age_Group', 'Region', 'Attitude_Score', 'Contribution_Score', 'Last_Active_Days_Ago']],
    use_container_width=True,
    hide_index=True
)

if not risk_df.empty:
    st.warning(f"⚠️ Action Required: **{len(risk_df)} users** identified as High-Risk Influencers. Recommendation: Trigger 'Doubt-Specific' email campaign.")
else:
    st.success("✅ No high-risk segments identified with current filters.")
