import streamlit as st
import pandas as pd
import altair as alt
from utils import load_css
from backend import SessionManager

st.set_page_config(page_title="My Performance", page_icon="📈", layout="wide")
load_css()
stats = SessionManager.get_stats()

# Custom CSS for Performance
st.markdown("""
<style>
    .score-card {
        background-color: #1E1E2E;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #2B2B40;
        text-align: center;
    }
    .score-val { font-size: 36px; font-weight: 700; color: #FFFFFF; }
    .score-label { font-size: 14px; color: #A0A0B0; }
    .score-change { font-size: 12px; font-weight: 600; }
    .pos { color: #00F260; }
    .neg { color: #FF4B4B; }
    
    .skill-row {
        margin-bottom: 15px;
    }
    .skill-label {
        display: flex;
        justify-content: space-between;
        color: #FFFFFF;
        font-size: 14px;
        margin-bottom: 5px;
    }
    .progress-bg {
        width: 100%;
        height: 8px;
        background-color: #2B2B40;
        border-radius: 4px;
    }
    .progress-fill {
        height: 100%;
        border-radius: 4px;
    }
    
    .action-card {
        background-color: #1E1E2E;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #2B2B40;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
</style>
""", unsafe_allow_html=True)

st.title("McKinsey Retail Growth Strategy")
st.caption("Completed: October 26, 2023")

# Score Overview
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown("""
    <div class="score-card">
        <div class="score-label">Overall Score</div>
        <div class="score-val">82/100</div>
        <div class="score-change pos">+5% vs. avg</div>
    </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown("""
    <div class="score-card">
        <div class="score-label">Problem Structuring</div>
        <div class="score-val">90%</div>
        <div class="score-change pos">+8% vs. avg</div>
    </div>
    """, unsafe_allow_html=True)
with c3:
    st.markdown("""
    <div class="score-card">
        <div class="score-label">Quantitative Analysis</div>
        <div class="score-val">65%</div>
        <div class="score-change neg">-3% vs. avg</div>
    </div>
    """, unsafe_allow_html=True)
with c4:
    st.markdown("""
    <div class="score-card">
        <div class="score-label">Communication</div>
        <div class="score-val">95%</div>
        <div class="score-change pos">+2% vs. avg</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

col_skills, col_actions = st.columns([1, 1])

with col_skills:
    st.markdown("### Core Competency Breakdown")
    
    skills = stats['skills']
    colors = {
        'Problem Structuring': '#6C63FF',
        'Quantitative Analysis': '#FF9F0A',
        'Business Acumen': '#00F260',
        'Communication': '#64D2FF',
        'Synthesis': '#FF4B4B'
    }
    
    for skill, score in skills.items():
        color = colors.get(skill, '#6C63FF')
        st.markdown(f"""
        <div class="skill-row">
            <div class="skill-label">
                <span>{skill}</span>
                <span>{score}%</span>
            </div>
            <div class="progress-bg">
                <div class="progress-fill" style="width: {score}%; background-color: {color};"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with col_actions:
    st.markdown("### Areas for Improvement")
    st.info("💡 **Calculation speed** was slow during the market sizing question, impacting timing.")
    st.warning("⚠️ Did not fully synthesize the final recommendation; it lacked a clear 'so what'.")
    
    st.markdown("### Action Plan: Your Next Steps")
    
    st.markdown("""
    <div class="action-card">
        <div>
            <div style="font-weight: 600;">Drill 3 market sizing cases.</div>
            <div style="font-size: 12px; color: #A0A0B0;">Focus on improving calculation speed.</div>
        </div>
        <button style="background: #2B2B40; color: #6C63FF; border: 1px solid #6C63FF; padding: 5px 10px; border-radius: 4px;">Start Drill</button>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="action-card">
        <div>
            <div style="font-weight: 600;">Watch video on effective synthesis.</div>
            <div style="font-size: 12px; color: #A0A0B0;">Learn how to deliver a powerful final recommendation.</div>
        </div>
        <button style="background: #2B2B40; color: #6C63FF; border: 1px solid #6C63FF; padding: 5px 10px; border-radius: 4px;">Watch Now</button>
    </div>
    """, unsafe_allow_html=True)
