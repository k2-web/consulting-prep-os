import streamlit as st
import time
import random
from utils import load_css
from backend import SessionManager

st.set_page_config(page_title="Active Case", page_icon="⏱️", layout="wide")
load_css()
SessionManager.init_session()

# --- Configuration ---
# --- Configuration ---
STAGES = ["Introduction", "Framework", "Market Sizing", "Brainstorming", "Conclusion"]

# Load Case Context from Session State or Default
if 'selected_case' in st.session_state:
    selected = st.session_state['selected_case']
    CASE_CONTEXT = {
        "company": selected['title'],
        "industry": selected['industry'],
        "problem": selected['desc'],
        "goal": "Solve the case objectives" # Generic goal if not in data, or could be added to case data
    }
else:
    # Fallback / Default
    CASE_CONTEXT = {
        "company": "AeroWidget Inc.",
        "industry": "Manufacturing",
        "problem": "Declining profits (20% drop)",
        "goal": "Identify root cause and turnaround strategy"
    }

# --- State Management ---
# --- State Management ---
# Check if we need to reset the state (new case selected)
if "current_case_title" not in st.session_state or st.session_state.current_case_title != CASE_CONTEXT['company']:
    st.session_state.case_state = {
        "stage_index": 0,
        "messages": [],
        "history": [], 
        "start_time": time.time(),
        "timer_paused": False,
        "timer_remaining": 1500, # 25 mins
        "stage_complete": False # Track if user can move on
    }
    st.session_state.current_case_title = CASE_CONTEXT['company']
    
    # Initial Message
    welcome_msg = f"Hello Tanvi. I'm the Case Lead. We are looking at '{CASE_CONTEXT['company']}', a {CASE_CONTEXT['industry']} company. \n\n**Situation**: {CASE_CONTEXT['problem']}.\n\nTake a moment to gather your thoughts. When ready, ask any clarifying questions."
    st.session_state.case_state["messages"].append({"role": "assistant", "content": welcome_msg})

if "case_state" not in st.session_state:
    # Should be handled above, but safety fallback
    st.session_state.case_state = {
        "stage_index": 0,
        "messages": [],
        "history": [], 
        "start_time": time.time(),
        "timer_paused": False,
        "timer_remaining": 1500,
        "stage_complete": False
    }

def advance_stage():
    current_idx = st.session_state.case_state["stage_index"]
    if current_idx < len(STAGES) - 1:
        st.session_state.case_state["stage_index"] += 1
        st.session_state.case_state["stage_complete"] = False # Reset for next stage
        
        # Add stage transition message
        next_stage = STAGES[current_idx + 1]
        st.session_state.case_state["messages"].append({
            "role": "assistant", 
            "content": f"**Moving to {next_stage}**. {get_stage_prompt(next_stage)}"
        })
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

# --- Gemini AI Engine ---
import google.generativeai as genai

class CaseBrain:
    def __init__(self):
        self.api_key = None
        self.model = None
        self.model_id = "gemini-2.5-flash" # Updated to available model
        self.history_buffer = [] 
        
        # Try to load API Key
        try:
            if "GEMINI_API_KEY" in st.secrets:
                self.api_key = st.secrets["GEMINI_API_KEY"]
            elif "general" in st.secrets and "GEMINI_API_KEY" in st.secrets["general"]:
                self.api_key = st.secrets["general"]["GEMINI_API_KEY"]
                
            if self.api_key:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-2.5-flash')
        except Exception as e:
            print(f"API Init Error: {e}")
            
        self.score_card = {
            "Structure": 50,
            "Analysis": 50,
            "Communication": 50
        }

    def generate_response(self, user_input, stage):
        """
        Generates a response using Gemini.
        """
        # 1. Check for "Pass" keywords
        if any(w in user_input.lower() for w in ["next", "move on", "proceed", "conclusion"]):
            st.session_state.case_state["stage_complete"] = True
            return "You seem ready to move on. I've enabled the 'Next Stage' button for you."

        # 2. API Call
        if self.model:
            try:
                # Construct Prompt
                system_instruction = f"""
                You are a Case Interviewer at a top consulting firm (McKinsey/BCG style).
                Case: AeroWidget Inc. (Manufacturing, Declining Profits).
                Current Stage: {stage}.
                
                Your Goal:
                - Guide the candidate (Tanvi) through the case.
                - Be professional, encouraging, but rigorous.
                - Do NOT give the answer away. Ask guiding questions.
                - If they ask for data, provide it ONLY if it fits the current stage.
                - Keep responses concise (max 3 sentences).
                
                Data Context:
                - Revenue: Down 15% YoY.
                - Costs: Flat.
                - Price: Stable.
                - Volume: Down 15%.
                - Market: Growing 3% (so Market Share is down).
                - Competitor: 'BudgetWidget' entered 18 months ago with lower prices.
                """
                
                # Add user message to buffer
                self.history_buffer.append(f"Candidate: {user_input}")
                
                # Create context window
                context = "\n".join(self.history_buffer[-10:])
                
                # Generate
                response = self.model.generate_content(
                    f"{system_instruction}\n\nConversation History:\n{context}\n\nInterviewer Response:"
                )
                
                reply = response.text
                self.history_buffer.append(f"Interviewer: {reply}")
                
                return reply
                
            except Exception as e:
                # Rate Limit or Auth Error
                if "429" in str(e) or "quota" in str(e).lower():
                    return "⚠️ Free limits expired. Please try again later."
                
                # DEBUG: Show actual error in UI
                st.error(f"API Connection Error: {e}")
                
                print(f"API Error: {e}")
                return self._get_fallback(user_input)
        else:
            return self._get_fallback(user_input)

    def evaluate_performance(self):
        """Generates a final evaluation using the API."""
        if not self.model:
            return self.score_card
            
        try:
            context = "\n".join(self.history_buffer)
            prompt = f"""
            Analyze the following case interview transcript for AeroWidget Inc.
            Candidate: Tanvi.
            
            Transcript:
            {context}
            
            Task:
            Provide a score (0-100) for:
            1. Structure
            2. Analysis
            3. Communication
            
            Output format: JSON with keys 'Structure', 'Analysis', 'Communication'.
            """
            
            response = self.model.generate_content(prompt)
            
            # Try to parse JSON from text (Gemini 1.5 Flash is good at this)
            import json
            import re
            text = response.text
            # Find JSON block
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                return json.loads(match.group(0))
            return self.score_card
        except Exception as e:
            print(f"Eval Error: {e}")
            return self.score_card

    def _get_fallback(self, text):
        # Fallback to the old logic if API fails
        return "I'm having trouble connecting to the server (API Error). But let's continue. What are your thoughts on the drivers?"

# Initialize Brain
if "brain" not in st.session_state:
    st.session_state.brain = CaseBrain()

def generate_response(user_input, stage):
    """Proxy function to call the brain."""
    return st.session_state.brain.generate_response(user_input, stage)

# --- UI Layout ---

# Sidebar
with st.sidebar:
    st.markdown("### Timer")
    
    # Timer Controls
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⏸ Pause"):
            st.session_state.case_state["timer_paused"] = True
    with c2:
        if st.button("▶ Resume"):
            st.session_state.case_state["timer_paused"] = False
            
    # JavaScript Timer (Pauseable)
    is_paused = "true" if st.session_state.case_state["timer_paused"] else "false"
    st.components.v1.html(
        f"""
        <div style="text-align: center; font-family: monospace; font-size: 32px; color: #6C63FF; background: #1E1E2E; padding: 10px; border-radius: 8px; border: 1px solid #2B2B40;">
            <span id="time">25:00</span>
        </div>
        <script>
        var paused = {is_paused};
        var duration = 60 * 25;
        var display = document.querySelector('#time');
        
        var timer = duration, minutes, seconds;
        
        // Try to restore state if possible, or just run
        // Note: In a real app, we'd sync this with Streamlit state more tightly
        
        setInterval(function () {{
            if (!paused) {{
                minutes = parseInt(timer / 60, 10);
                seconds = parseInt(timer % 60, 10);

                minutes = minutes < 10 ? "0" + minutes : minutes;
                seconds = seconds < 10 ? "0" + seconds : seconds;

                display.textContent = minutes + ":" + seconds;

                if (--timer < 0) {{
                    timer = duration;
                }}
            }} else {{
                display.textContent = "PAUSED";
            }}
        }}, 1000);
        </script>
        """,
        height=80
    )
    
    st.markdown("### Key Objectives")
    objectives = [
        "Clarify the client's objective.",
        "Structure a Profitability Framework.",
        "Calculate US Market Size.",
        "Brainstorm Strategic Options.",
        "Deliver a Synthesis."
    ]
    for obj in objectives:
        st.markdown(f'<div style="background-color: #1E1E2E; padding: 10px; border-radius: 6px; margin-bottom: 8px; border-left: 3px solid #00F260; font-size: 13px;">{obj}</div>', unsafe_allow_html=True)
        
    st.markdown("---")
    if st.button("End Case & Save", type="primary"):
        with st.spinner("Analyzing your performance with AI..."):
            # Save with detailed breakdown from AI
            scores = st.session_state.brain.evaluate_performance()
            SessionManager.save_interview("AeroWidget Inc.", "Completed", score=scores)
        st.switch_page("pages/3_My_Performance.py")

# Header
col_header, col_actions = st.columns([3, 1])
with col_header:
    st.title(f"Case: {CASE_CONTEXT['company']}")
    st.caption(f"{CASE_CONTEXT['problem']} | {CASE_CONTEXT['industry']}")

# Progress
current_stage_idx = st.session_state.case_state["stage_index"]
current_stage_name = STAGES[current_stage_idx]
progress_val = (current_stage_idx + 1) / len(STAGES)
st.progress(progress_val)
st.caption(f"Stage {current_stage_idx + 1}/{len(STAGES)}: **{current_stage_name}**")

# Main Interface
tab1, tab2 = st.tabs(["Interview Interface", "My Notes"])

with tab1:
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
            
        # AI Logic
        with st.spinner("Interviewer is thinking..."):
            time.sleep(0.8) # Simulate delay
            response = generate_response(prompt, current_stage_name)
            
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.case_state["messages"].append({"role": "assistant", "content": response})
        
        # Rerun to update button state if stage complete
        if st.session_state.case_state["stage_complete"]:
            st.rerun()
        
    # Stage Control - Only show if complete!
    if st.session_state.case_state["stage_complete"]:
        st.success("✅ Stage Complete! You have uncovered the key insights.")
        if st.button(f"Move to Next Stage ({STAGES[min(current_stage_idx+1, len(STAGES)-1)]})", type="primary"):
            advance_stage()

with tab2:
    st.text_area("Scratchpad", height=400, placeholder="Use this space for calculations, structures, and notes...")
