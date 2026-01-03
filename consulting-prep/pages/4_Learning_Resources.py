import streamlit as st
from utils import load_css
import os

st.set_page_config(page_title="Learning Resources", page_icon="📖", layout="wide")
load_css()

# --- Content Loading Helper ---
def load_markdown(filename):
    try:
        with open(os.path.join("consulting-prep/content", filename), "r") as f:
            return f.read()
    except FileNotFoundError:
        return "Content not found."

# --- State Management for Navigation ---
if "viewing_resource" not in st.session_state:
    st.session_state.viewing_resource = None

def view_resource(resource_id):
    st.session_state.viewing_resource = resource_id
    st.rerun()

def back_to_library():
    st.session_state.viewing_resource = None

# --- Main Page Logic ---
if st.session_state.viewing_resource:
    # === DETAIL VIEW ===
    res = st.session_state.viewing_resource
    
    st.button("← Back to Library", on_click=back_to_library)
    st.markdown(f"# {res['title']}")
    
    if res['type'] == 'markdown':
        content = load_markdown(res['file'])
        st.markdown(content)
    elif res['type'] == 'video':
        st.video(res['url'])
        st.info(f"**Description**: {res['desc']}")

else:
    # === MASTER VIEW (Library) ===
    st.title("Learning Resources")
    st.caption("Curated guides, frameworks, and expert advice to master the case interview.")

    # Featured Guide
    with st.container():
        st.markdown("""
        <div style="background: linear-gradient(90deg, #1E1E2E 0%, #2D2B55 100%); border-radius: 12px; padding: 30px; border: 1px solid #2B2B40; margin-bottom: 30px;">
            <div style="color: #6C63FF; font-weight: 700; text-transform: uppercase; font-size: 12px; margin-bottom: 10px;">Featured Guide</div>
            <h2 style="margin: 0 0 10px 0;">The Ultimate Guide to Market Sizing</h2>
            <p style="color: #A0A0B0; max-width: 600px;">Master a critical case interview skill with our comprehensive new guide.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Read Featured Guide", type="primary"):
            view_resource({
                "title": "Market Sizing Guide",
                "type": "markdown",
                "file": "market_entry.md", # Reusing market entry for demo or create new
                "desc": "Master market sizing."
            })

    st.markdown("### Core Consulting Frameworks")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### Porter's Five Forces")
        st.caption("Analyze industry structure.")
        if st.button("Read Guide", key="btn_porter"):
            view_resource({
                "title": "Porter's Five Forces",
                "type": "markdown",
                "file": "market_entry.md",
                "desc": "Industry Analysis"
            })
            
    with col2:
        st.markdown("#### Profitability Framework")
        st.caption("Revenue vs Cost analysis.")
        if st.button("Read Guide", key="btn_profit"):
            view_resource({
                "title": "Profitability Framework",
                "type": "markdown",
                "file": "profitability.md",
                "desc": "Profitability"
            })
            
    with col3:
        st.markdown("#### Behavioral Interviews")
        st.caption("Master the 'Fit' questions.")
        if st.button("Read Guide", key="btn_behavioral"):
            view_resource({
                "title": "Behavioral & Culture",
                "type": "markdown",
                "file": "behavioral.md",
                "desc": "Behavioral"
            })

    st.markdown("---")
    st.markdown("### Expert Video Library")
    
    v1, v2, v3 = st.columns(3)
    
    with v1:
        st.image("https://img.youtube.com/vi/dCxSsr5xu-s/0.jpg", use_container_width=True)
        st.markdown("**Case Interview 101**")
        if st.button("Watch Video", key="vid_1"):
            view_resource({
                "title": "Case Interview 101",
                "type": "video",
                "url": "https://www.youtube.com/watch?v=dCxSsr5xu-s",
                "desc": "A comprehensive overview by Victor Cheng."
            })
            
    with v2:
        st.image("https://img.youtube.com/vi/4jG-OgM2q_w/0.jpg", use_container_width=True)
        st.markdown("**Market Sizing Demo**")
        if st.button("Watch Video", key="vid_2"):
            view_resource({
                "title": "Market Sizing Demo",
                "type": "video",
                "url": "https://www.youtube.com/watch?v=4jG-OgM2q_w",
                "desc": "Real-time market sizing demonstration."
            })
            
    with v3:
        st.image("https://img.youtube.com/vi/0p7gCwyd1EU/0.jpg", use_container_width=True)
        st.markdown("**Thinking Like a Consultant**")
        if st.button("Watch Video", key="vid_3"):
            view_resource({
                "title": "Thinking Like a Consultant",
                "type": "video",
                "url": "https://www.youtube.com/watch?v=0p7gCwyd1EU",
                "desc": "Mindset shifts for success."
            })

    st.markdown("### Advanced Prep")
    v4, v5, v6 = st.columns(3)
    
    with v4:
        st.image("https://img.youtube.com/vi/f0C135xS3t4/0.jpg", use_container_width=True)
        st.markdown("**McKinsey PEI (Behavioral)**")
        if st.button("Watch Video", key="vid_4"):
            view_resource({
                "title": "McKinsey PEI Guide",
                "type": "video",
                "url": "https://www.youtube.com/watch?v=f0C135xS3t4",
                "desc": "Mastering the Personal Experience Interview."
            })
            
    with v5:
        st.image("https://img.youtube.com/vi/7qR1V9j0tzM/0.jpg", use_container_width=True)
        st.markdown("**Consulting Resume Tips**")
        if st.button("Watch Video", key="vid_5"):
            view_resource({
                "title": "Consulting Resume Guide",
                "type": "video",
                "url": "https://www.youtube.com/watch?v=7qR1V9j0tzM",
                "desc": "How to get the interview."
            })
            
    with v6:
        st.image("https://img.youtube.com/vi/Revk4x6tqM4/0.jpg", use_container_width=True)
        st.markdown("**Structuring Complex Cases**")
        if st.button("Watch Video", key="vid_6"):
            view_resource({
                "title": "Advanced Structuring",
                "type": "video",
                "url": "https://www.youtube.com/watch?v=Revk4x6tqM4",
                "desc": "Moving beyond standard frameworks."
            })
