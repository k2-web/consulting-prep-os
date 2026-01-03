import streamlit as st
import base64

def load_css():
    """
    Injects the 'ConsultPrep' Ultra-Premium CSS.
    """
    st.markdown("""
    <style>
        /* Import Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;700&display=swap');

        /* Global Reset & Theme */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            background-color: #13131A; /* Deepest Dark Blue/Black */
            color: #FFFFFF !important;
        }
        
        /* Force Text Color on all common elements */
        p, h1, h2, h3, h4, h5, h6, span, div, label, .stMarkdown, .stCaption {
            color: #FFFFFF !important;
        }
        
        /* Specific overrides for muted text if needed, but default to white for now as requested */
        .stCaption {
            color: #E0E0E0 !important; /* Slightly off-white for captions */
        }
        
        /* Streamlit Main Container */
        .stApp {
            background-color: #13131A;
        }
        
        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #181820;
            border-right: 1px solid #2B2B40;
        }
        
        /* Headings */
        h1, h2, h3 {
            font-weight: 700;
            letter-spacing: -0.5px;
        }
        
        /* Buttons (Primary - Purple) */
        .stButton > button {
            background-color: #6C63FF;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 24px;
            font-weight: 600;
            transition: all 0.2s ease;
        }
        .stButton > button:hover {
            background-color: #5a52d5;
            box-shadow: 0 4px 12px rgba(108, 99, 255, 0.3);
        }
        
        /* Buttons (Secondary - Dark) */
        .stButton > button[kind="secondary"] {
            background-color: #2B2B40;
            color: #FFFFFF;
            border: 1px solid #3E3E50;
        }
        
        /* Inputs & Selectboxes */
        .stTextInput > div > div > input, .stSelectbox > div > div > div {
            background-color: #1E1E2E;
            color: white;
            border: 1px solid #2B2B40;
            border-radius: 8px;
        }
        
        /* Cards (General Utility Class) */
        .card {
            background-color: #1E1E2E;
            border-radius: 12px;
            padding: 24px;
            border: 1px solid #2B2B40;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        /* Progress Bars */
        .stProgress > div > div > div > div {
            background-color: #6C63FF;
        }
        
        /* Metrics */
        [data-testid="stMetricValue"] {
            font-family: 'Inter', sans-serif;
            font-weight: 700;
        }
        
        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #13131A;
        }
        ::-webkit-scrollbar-thumb {
            background: #2B2B40;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #6C63FF;
        }
        
        /* Hide Streamlit Branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
    </style>
    """, unsafe_allow_html=True)

def render_header():
    """
    Renders the ConsultPrep Header (Logo + Nav).
    """
    st.markdown("""
    <div style="display: flex; align-items: center; justify-content: space-between; padding: 20px 0; margin-bottom: 30px; border-bottom: 1px solid #2B2B40;">
        <div style="display: flex; align-items: center;">
            <div style="width: 32px; height: 32px; background: linear-gradient(135deg, #6C63FF 0%, #00F260 100%); border-radius: 8px; margin-right: 12px;"></div>
            <div style="font-size: 20px; font-weight: 700; letter-spacing: -0.5px;">ConsultPrep</div>
        </div>
        <div style="display: flex; gap: 24px; font-size: 14px; color: #A0A0B0;">
            <span style="color: #fff; font-weight: 500;">Dashboard</span>
            <span>Case Library</span>
            <span>Drills</span>
            <span>Profile</span>
        </div>
        <div style="display: flex; align-items: center; gap: 16px;">
            <div style="width: 36px; height: 36px; background-color: #2B2B40; border-radius: 50%; display: flex; align-items: center; justify-content: center;">🔔</div>
            <div style="width: 36px; height: 36px; background-color: #E0E0E0; border-radius: 50%; border: 2px solid #6C63FF;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar_footer():
    """Renders the version tag in the sidebar."""
    with st.sidebar:
        st.markdown("---")
        st.markdown(
            """
            <div style="text-align: center; color: #666; font-size: 12px;">
                ConsultPrep OS v6.0<br>
                © 2025
            </div>
            """, 
            unsafe_allow_html=True
        )
