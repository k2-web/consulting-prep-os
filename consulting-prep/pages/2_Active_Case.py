import streamlit as st
import time
import random
from utils import load_css
from backend import SessionManager

st.set_page_config(page_title="Active Case", page_icon="⏱️", layout="wide")
load_css()
SessionManager.init_session()

# --- Configuration ---
STAGES = ["Introduction", "Framework", "Market Sizing", "Brainstorming", "Conclusion"]
CASE_CONTEXT = {
    "company": "AeroWidget Inc.",
    "industry": "Manufacturing",
    "problem": "Declining profits (20% drop)",
    "goal": "Identify root cause and turnaround strategy"
}

# --- State Management ---
if "case_state" not in st.session_state:
    st.session_state.case_state = {
        "stage_index": 0,
        "messages": [],
        "history": [], # For saving later
        "start_time": time.time()
    }
    # Initial Message
    welcome_msg = f"Hello Tanvi. I'm the Case Lead. We are looking at '{CASE_CONTEXT['company']}', a widget manufacturer facing declining profits. \n\n**Objective**: {CASE_CONTEXT['goal']}.\n\nTake a moment to gather your thoughts. When ready, ask any clarifying questions."
    st.session_state.case_state["messages"].append({"role": "assistant", "content": welcome_msg})

def advance_stage():
    current_idx = st.session_state.case_state["stage_index"]
    if current_idx < len(STAGES) - 1:
        st.session_state.case_state["stage_index"] += 1
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

# --- Advanced Mock-AI Engine ---
class CaseBrain:
    def __init__(self):
        self.context = {
            "revenue_analyzed": False,
            "costs_analyzed": False,
            "volume_checked": False,
            "price_checked": False,
            "competitors_checked": False,
            "market_growth_checked": False,
            "customer_seg_checked": False
        }
        
    def generate_response(self, user_input, stage):
        """
        Generates a context-aware response using templates and keyword matching.
        To upgrade to Real AI: Replace this method with an OpenAI API call.
        """
        user_input = user_input.lower()
        
        # 1. Check for "Pass" keywords to nudge user
        if any(w in user_input for w in ["next", "move on", "proceed", "conclusion"]):
            return "You seem ready to move on. Please hit the 'Move to Next Stage' button below."

        # 2. Stage-Specific Logic
        if stage == "Introduction":
            return self._handle_intro(user_input)
        elif stage == "Framework":
            return self._handle_framework(user_input)
        elif stage == "Market Sizing":
            return self._handle_market_sizing(user_input)
        elif stage == "Brainstorming":
            return self._handle_brainstorming(user_input)
        elif stage == "Conclusion":
            return "Please deliver your final recommendation in a structured format (Recommendation, Reasons, Risks, Next Steps)."
            
        return self._get_fallback()

    def _handle_intro(self, text):
        # Business Model
        if any(w in text for w in ["business model", "how do we make money", "revenue stream"]):
            return random.choice([
                "We are a B2B manufacturer. We sell high-precision widgets directly to large industrial clients.",
                "Our business model is standard B2B. We manufacture widgets and sell them to 3 major industrial sectors.",
                "Think of us as a component supplier. We sell directly to OEMs (Original Equipment Manufacturers)."
            ])
        # Geography
        if any(w in text for w in ["geography", "location", "region", "us", "global"]):
            return "We operate globally, but 80% of our revenue comes from the US market. The decline is specifically in the US."
        # Goal
        if any(w in text for w in ["goal", "target", "objective", "timeline"]):
            return "The CEO wants to reverse the 20% profit decline and return to growth within 12 months."
            
        return "That's a fair question. We sell premium widgets to B2B clients, mostly in the US. What else would you like to clarify?"

    def _handle_framework(self, text):
        # Revenue
        if "revenue" in text:
            self.context["revenue_analyzed"] = True
            return "Looking at Revenue is key. Our data shows Revenue is down 15% year-over-year. Costs are flat."
        # Costs
        if "cost" in text or "expense" in text:
            self.context["costs_analyzed"] = True
            return "Costs have remained flat. We haven't seen any major spikes in raw materials or labor. So the issue is likely on the revenue side."
        # Price vs Volume
        if "price" in text:
            self.context["price_checked"] = True
            return "Prices have remained stable. We haven't changed our pricing strategy in 2 years."
        if "volume" in text or "units" in text:
            self.context["volume_checked"] = True
            return "Bingo. Volume is down 15%. We are selling fewer units. Why do you think that is?"
        # Competition
        if "competitor" in text or "market share" in text:
            self.context["competitors_checked"] = True
            return "Good instinct. We have lost market share to a new entrant, 'BudgetWidget', who entered the market 18 months ago."
            
        return "That's a valid area to investigate. Remember, Profit = (Price * Volume) - (Fixed + Variable Costs). Where does the data point you?"

    def _handle_market_sizing(self, text):
        # Population
        if "330" in text or "population" in text:
            return "Using the US population (330M) is a good start, but remember we are B2B. Maybe start with the number of industrial companies?"
        # Calculation check
        if any(c in text for c in ["10 million", "10m", "10,000,000"]):
            return "10 Million units seems like a reasonable estimate for the total market size. Since we sold 1M units last year, we have about 10% market share."
        # Growth
        if "grow" in text or "shrink" in text:
            self.context["market_growth_checked"] = True
            return "The overall market is actually growing by 3% per year. So demand isn't the issue."
            
        return "Walk me through your logic. Start with the top-down approach. How many potential buyers exist in the US?"

    def _handle_brainstorming(self, text):
        # Price Cut
        if "lower price" in text or "cut price" in text:
            return "We could lower prices, but we are a premium brand. A price war might destroy our margins. What else?"
        # New Product
        if "new product" in text or "innovate" in text:
            return "Innovation is a strong option. We could launch a 'Lite' version of our widget to compete with the low-cost entrant."
        # Marketing
        if "market" in text or "sales" in text:
            return "Increasing sales effort could help, but if our product is too expensive, marketing alone might not fix it."
        # Acquisition
        if "acquire" in text or "buy" in text:
            return "Acquiring the competitor is bold. It would be expensive but would instantly restore market share. What are the risks?"
            
        return "Those are good ideas. Consider the 'Ansoff Matrix' - Market Penetration, Product Development, Market Development, or Diversification."

    def _get_fallback(self):
        templates = [
            "That's an interesting perspective. Tell me more about how that impacts the bottom line.",
            "I see where you're going. Can you quantify that impact?",
            "Good thought. Let's dig a bit deeper into that specific driver.",
            "Okay, noted. What implies for our overall strategy?",
            "Let's take a step back. What does the data suggest?"
        ]
        return random.choice(templates)

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
    # JavaScript Timer
    st.components.v1.html(
        """
        <div style="text-align: center; font-family: monospace; font-size: 32px; color: #6C63FF; background: #1E1E2E; padding: 10px; border-radius: 8px; border: 1px solid #2B2B40;">
            <span id="time">25:00</span>
        </div>
        <script>
        function startTimer(duration, display) {
            var timer = duration, minutes, seconds;
            setInterval(function () {
                minutes = parseInt(timer / 60, 10);
                seconds = parseInt(timer % 60, 10);

                minutes = minutes < 10 ? "0" + minutes : minutes;
                seconds = seconds < 10 ? "0" + seconds : seconds;

                display.textContent = minutes + ":" + seconds;

                if (--timer < 0) {
                    timer = duration;
                }
            }, 1000);
        }
        startTimer(60 * 25, document.querySelector('#time'));
        </script>
        """,
        height=70
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
        final_score = random.randint(75, 95)
        SessionManager.save_interview("AeroWidget Inc.", "Completed", score=final_score)
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
        
    # Manual Stage Control (Fix for "Only 2 replies")
    st.markdown("---")
    col_prev, col_next = st.columns([1, 5])
    with col_next:
        if st.button(f"Move to Next Stage ({STAGES[min(current_stage_idx+1, len(STAGES)-1)]})", type="secondary"):
            advance_stage()

with tab2:
    st.text_area("Scratchpad", height=400, placeholder="Use this space for calculations, structures, and notes...")
