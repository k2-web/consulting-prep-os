import streamlit as st
import time
import random
from utils import load_css
from backend import SessionManager

st.set_page_config(page_title="Active Case", page_icon="⏱️", layout="wide")
load_css()
SessionManager.init_session()

# --- State Machine Logic ---
STAGES = ["Introduction", "Framework", "Market Sizing", "Brainstorming", "Conclusion"]

if "case_state" not in st.session_state:
    st.session_state.case_state = {
        "stage_index": 0,
        "messages": [],
        "feedback_log": [],
        "scores": []
    }
    # Initial Message
    st.session_state.case_state["messages"].append({
        "role": "assistant", 
        "content": "Hello Tanvi. I'm the Case Lead. We are looking at 'AeroWidget Inc.', a widget manufacturer facing declining profits. \n\n**Objective**: Identify the root cause and recommend a turnaround strategy.\n\nTake a moment to gather your thoughts. When ready, ask any clarifying questions."
    })

def advance_stage():
    current_idx = st.session_state.case_state["stage_index"]
    if current_idx < len(STAGES) - 1:
        st.session_state.case_state["stage_index"] += 1
        st.rerun()

def get_stage_prompt(stage_name):
    prompts = {
        "Introduction": "Ask clarifying questions about the business model and goal.",
        "Framework": "Structure your approach. How will you isolate the profit decline?",
        "Market Sizing": "Let's estimate the US market size for widgets. Walk me through your logic.",
        "Brainstorming": "Competitors dropped prices. What are our strategic options?",
        "Conclusion": "Synthesize your findings and give a final recommendation."
    }
    return prompts.get(stage_name, "")

# --- UI Layout ---

# Custom CSS
st.markdown("""
<style>
    .timer-box { background-color: #1E1E2E; padding: 20px; border-radius: 12px; text-align: center; margin-bottom: 20px; border: 1px solid #2B2B40; }
    .timer-display { font-size: 48px; font-weight: 700; color: #6C63FF; font-family: 'JetBrains Mono', monospace; }
    .objective-box { background-color: #1E1E2E; padding: 15px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid #00F260; }
    .stage-indicator { font-size: 14px; color: #A0A0B0; margin-bottom: 5px; }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### Timer")
    st.markdown("""
    <div class="timer-box">
        <div class="timer-display">25:00</div>
        <div style="color: #A0A0B0; font-size: 12px;">remaining</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Key Objectives")
    objectives = [
        "Clarify the client's objective.",
        "Structure a Profitability Framework.",
        "Calculate US Market Size.",
        "Brainstorm Strategic Options.",
        "Deliver a Synthesis."
    ]
    for obj in objectives:
        st.markdown(f'<div class="objective-box">{obj}</div>', unsafe_allow_html=True)

# Header
col_header, col_actions = st.columns([3, 1])
with col_header:
    st.title("Profitability Decline at 'AeroWidget Inc.'")
with col_actions:
    if st.button("End Case & Save", type="primary"):
        # Calculate Final Score
        final_score = random.randint(75, 95) # Simulation
        SessionManager.save_interview("AeroWidget Inc.", "Completed", score=final_score)
        st.switch_page("pages/3_My_Performance.py")

# Progress
current_stage_idx = st.session_state.case_state["stage_index"]
current_stage_name = STAGES[current_stage_idx]
progress_val = (current_stage_idx + 1) / len(STAGES)
st.progress(progress_val)
st.caption(f"Stage {current_stage_idx + 1} of {len(STAGES)}: **{current_stage_name}**")

# Main Interface
tab1, tab2 = st.tabs(["Interview Interface", "My Notes"])

with tab1:
    st.info(f"**Interviewer**: {get_stage_prompt(current_stage_name)}")
    
    # Chat History
    for msg in st.session_state.case_state["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    # Input
    if prompt := st.chat_input("Type your response..."):
        # User Message
        st.session_state.case_state["messages"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # AI Logic (Simulation)
        response = ""
        if current_stage_name == "Introduction":
            response = "Good questions. We sell premium widgets directly to businesses. Our goal is to reverse the 20% profit decline within 1 year. Please propose a framework."
            if "framework" in prompt.lower() or "structure" in prompt.lower():
                advance_stage()
                
        elif current_stage_name == "Framework":
            response = "That's a solid structure (Revenue vs Cost). Data shows Revenues are down due to Volume, while Costs are flat. Let's look at the market size to see if demand is shrinking."
            advance_stage()
            
        elif current_stage_name == "Market Sizing":
            response = "Your logic holds up. ~10M units/year seems accurate. The market is actually growing, so it's our market share that is shrinking. Competitors have slashed prices. Thoughts?"
            advance_stage()
            
        elif current_stage_name == "Brainstorming":
            response = "Price war is risky. Differentiation or Cost Cutting might be better. Let's wrap up. Please summarize your recommendation."
            advance_stage()
            
        elif current_stage_name == "Conclusion":
            response = "Thank you, Tanvi. That was a clear recommendation. We'll be in touch."
            st.balloons()
            
        # Assistant Message
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.case_state["messages"].append({"role": "assistant", "content": response})

with tab2:
    st.text_area("Case Notes", height=400, placeholder="Type your structure and calculations here...")
