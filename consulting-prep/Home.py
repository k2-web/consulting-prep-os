import streamlit as st
import pandas as pd
import altair as alt
from utils import load_css, render_header
from backend import SessionManager

# Page Configuration
st.set_page_config(
    page_title="ConsultPrep | Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Initialize Session & Theme
load_css()
SessionManager.init_session()
stats = SessionManager.get_stats()

# Custom CSS for Dashboard
st.markdown("""
<style>
    .stat-card {
        background-color: #1E1E2E;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #2B2B40;
    }
    .stat-value {
        font-size: 32px;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 5px;
    }
    .stat-label {
        font-size: 14px;
        color: #A0A0B0;
    }
    .stat-change {
        font-size: 12px;
        font-weight: 600;
    }
    .positive { color: #00F260; }
    .negative { color: #FF4B4B; }
    
    .section-header {
        font-size: 20px;
        font-weight: 600;
        margin-top: 30px;
        margin-bottom: 15px;
        color: #FFFFFF;
    }
</style>
""", unsafe_allow_html=True)

# Top Bar
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("# Welcome back, Tanvi!")
with col2:
    if st.button("Start New Case", type="primary", use_container_width=True):
        st.switch_page("pages/1_Case_Library.py")

# Stats Row
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">Cases Completed</div>
        <div class="stat-value">{stats['cases_completed']}</div>
        <div class="stat-change positive">+5% this week</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">Average Score</div>
        <div class="stat-value">{stats['average_score']}%</div>
        <div class="stat-change positive">+2% this week</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    hours = int(stats['hours_practiced'])
    mins = int((stats['hours_practiced'] - hours) * 60)
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">Time Practiced</div>
        <div class="stat-value">{hours}h {mins}m</div>
        <div class="stat-change positive">+10% this week</div>
    </div>
    """, unsafe_allow_html=True)

# Performance Trend
st.markdown('<div class="section-header">Performance Trend</div>', unsafe_allow_html=True)

# Create Data for Chart
trend_data = pd.DataFrame({
    'Case': range(1, len(stats['trend']) + 1),
    'Score': stats['trend']
})

# Altair Chart
chart = alt.Chart(trend_data).mark_line(
    interpolate='monotone',
    strokeWidth=3,
    color='#6C63FF' # Purple accent
).encode(
    x=alt.X('Case', axis=None),
    y=alt.Y('Score', scale=alt.Scale(domain=[50, 100]), axis=None),
    tooltip=['Case', 'Score']
).properties(
    height=250,
    background='transparent'
).configure_view(
    strokeWidth=0
)

# Render Chart in a Card
st.markdown(f"""
<div class="stat-card" style="padding: 0px 20px 20px 20px;">
    <div style="padding-top: 20px; font-size: 24px; font-weight: 700;">{stats['average_score']}% Avg Score <span style="font-size: 14px; color: #00F260; margin-left: 10px;">+2%</span></div>
    <div style="color: #A0A0B0; font-size: 14px; margin-bottom: 20px;">Last 10 Cases</div>
</div>
""", unsafe_allow_html=True)
st.altair_chart(chart, use_container_width=True)


# Bottom Section: Continue Practicing & Upcoming
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown('<div class="section-header">Continue Practicing</div>', unsafe_allow_html=True)
    
    # Card 1
    st.markdown("""
    <div class="stat-card" style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 15px;">
        <div>
            <div style="font-weight: 600; font-size: 16px;">Market Sizing Drill</div>
            <div style="color: #A0A0B0; font-size: 12px;">Global Electric Vehicle Market</div>
            <div style="width: 100%; background-color: #2B2B40; height: 4px; border-radius: 2px; margin-top: 8px;">
                <div style="width: 40%; background-color: #6C63FF; height: 100%; border-radius: 2px;"></div>
            </div>
        </div>
        <div style="margin-left: 20px;">
             <a href="/Active_Case" target="_self" style="background-color: #2B2B40; color: #fff; padding: 8px 16px; border-radius: 6px; text-decoration: none; font-size: 12px;">Resume</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Card 2
    st.markdown("""
    <div class="stat-card" style="display: flex; align-items: center; justify-content: space-between;">
        <div>
            <div style="font-weight: 600; font-size: 16px;">Profitability Case</div>
            <div style="color: #A0A0B0; font-size: 12px;">Pharma Co. New Drug Launch</div>
            <div style="width: 100%; background-color: #2B2B40; height: 4px; border-radius: 2px; margin-top: 8px;">
                <div style="width: 70%; background-color: #6C63FF; height: 100%; border-radius: 2px;"></div>
            </div>
        </div>
        <div style="margin-left: 20px;">
             <a href="/Active_Case" target="_self" style="background-color: #2B2B40; color: #fff; padding: 8px 16px; border-radius: 6px; text-decoration: none; font-size: 12px;">Resume</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="section-header">Upcoming Cases</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="stat-card" style="margin-bottom: 15px;">
        <div style="display: flex; align-items: center;">
            <div style="background-color: #2B2B40; padding: 8px; border-radius: 6px; text-align: center; margin-right: 12px;">
                <div style="font-size: 10px; color: #6C63FF; font-weight: bold;">28</div>
                <div style="font-size: 10px; color: #A0A0B0;">OCT</div>
            </div>
            <div>
                <div style="font-weight: 600; font-size: 14px;">Tech M&A Case</div>
                <div style="color: #A0A0B0; font-size: 12px;">3:00 PM - with John D.</div>
            </div>
        </div>
    </div>
    
    <div class="stat-card">
        <div style="display: flex; align-items: center;">
            <div style="background-color: #2B2B40; padding: 8px; border-radius: 6px; text-align: center; margin-right: 12px;">
                <div style="font-size: 10px; color: #fff; font-weight: bold;">02</div>
                <div style="font-size: 10px; color: #A0A0B0;">NOV</div>
            </div>
            <div>
                <div style="font-weight: 600; font-size: 14px;">Retail Growth</div>
                <div style="color: #A0A0B0; font-size: 12px;">10:00 AM - with Sarah L.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
