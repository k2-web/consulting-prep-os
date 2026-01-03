import streamlit as st
from utils import load_css

# Page Configuration
st.set_page_config(
    page_title="ConsultPrep | Case Library",
    page_icon="📚",
    layout="wide",
)

load_css()

# Custom CSS for Case Cards
st.markdown("""
<style>
    .case-card {
        background-color: #1E1E2E;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #2B2B40;
        margin-bottom: 20px;
        transition: transform 0.2s;
    }
    .case-card:hover {
        transform: translateY(-5px);
        border-color: #6C63FF;
    }
    .case-title {
        font-size: 18px;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 10px;
    }
    .case-desc {
        font-size: 14px;
        color: #A0A0B0;
        margin-bottom: 15px;
        line-height: 1.5;
    }
    .tag {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
        margin-right: 8px;
    }
    .tag-tech { background-color: #2D2B55; color: #A599E9; }
    .tag-health { background-color: #1A3B34; color: #4CD964; }
    .tag-consumer { background-color: #4A2E2A; color: #FF9F0A; }
    .tag-finance { background-color: #1C3A5E; color: #64D2FF; }
    .tag-difficulty { background-color: #3A3A3A; color: #E0E0E0; }
    
    .time-badge {
        display: inline-flex;
        align-items: center;
        color: #A0A0B0;
        font-size: 12px;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Filters
with st.sidebar:
    st.markdown("### Filter Cases")
    search_query = st.text_input("Search by keyword...", placeholder="Search...")
    
    st.markdown("#### Difficulty")
    diff_filter = st.radio("Difficulty", ["All", "Beginner", "Intermediate", "Advanced"], label_visibility="collapsed")
    
    st.markdown("#### Industry")
    ind_filter = st.selectbox("Industry", ["All", "Technology", "Healthcare", "Consumer Goods", "Finance", "Energy"], label_visibility="collapsed")
    
    st.markdown("#### Case Type")
    type_filter = st.selectbox("Case Type", ["All", "Profitability", "Market Entry", "M&A", "Growth Strategy"], label_visibility="collapsed")
    
    # st.button("Apply Filters", type="primary", use_container_width=True) # Auto-update is better

# Main Content
col1, col2 = st.columns([3, 1])
with col1:
    st.title("Case Library")
    st.markdown("Browse and select from a library of consulting cases to practice.")
with col2:
    sort_opt = st.selectbox("Sort by", ["Most Popular", "Newest", "Hardest"], label_visibility="collapsed")

# Case Grid Data
all_cases = [
    {
        "title": "PharmaCo Growth Strategy",
        "desc": "Assessing market entry options for a new drug in the European market.",
        "tags": [("Healthcare", "tag-health"), ("Intermediate", "tag-difficulty")],
        "difficulty": "Intermediate",
        "industry": "Healthcare",
        "type": "Growth Strategy",
        "time": "20 min"
    },
    {
        "title": "Tech Startup Profitability",
        "desc": "Identifying key drivers of declining profits for a SaaS company.",
        "tags": [("Technology", "tag-tech"), ("Advanced", "tag-difficulty")],
        "difficulty": "Advanced",
        "industry": "Technology",
        "type": "Profitability",
        "time": "25 min"
    },
    {
        "title": "Retail Chain Expansion",
        "desc": "Should a coffee chain expand into the Asian market? Market sizing exercise.",
        "tags": [("Consumer Goods", "tag-consumer"), ("Beginner", "tag-difficulty")],
        "difficulty": "Beginner",
        "industry": "Consumer Goods",
        "type": "Market Entry",
        "time": "15 min"
    },
    {
        "title": "Airline M&A Analysis",
        "desc": "Evaluating the potential acquisition of a low-cost carrier by a legacy airline.",
        "tags": [("Finance", "tag-finance"), ("Advanced", "tag-difficulty")],
        "difficulty": "Advanced",
        "industry": "Finance",
        "type": "M&A",
        "time": "30 min"
    },
    {
        "title": "Social Media App Launch",
        "desc": "Estimate the market size for a new niche social media application in the US.",
        "tags": [("Technology", "tag-tech"), ("Beginner", "tag-difficulty")],
        "difficulty": "Beginner",
        "industry": "Technology",
        "type": "Market Entry",
        "time": "15 min"
    },
    {
        "title": "EV Manufacturer Cost Reduction",
        "desc": "Identify opportunities to reduce production costs for an electric vehicle.",
        "tags": [("Automotive", "tag-tech"), ("Intermediate", "tag-difficulty")],
        "difficulty": "Intermediate",
        "industry": "Technology", # Mapped Automotive to Tech/Energy broadly or keep separate
        "type": "Profitability",
        "time": "20 min"
    }
]

# Filter Logic
filtered_cases = []
for case in all_cases:
    # 1. Search
    if search_query and search_query.lower() not in case['title'].lower() and search_query.lower() not in case['desc'].lower():
        continue
    # 2. Difficulty
    if diff_filter != "All" and case['difficulty'] != diff_filter:
        continue
    # 3. Industry
    if ind_filter != "All" and case['industry'] != ind_filter:
        continue
    # 4. Type
    if type_filter != "All" and case['type'] != type_filter:
        continue
        
    filtered_cases.append(case)

# Render Grid (3 columns)
if not filtered_cases:
    st.info("No cases found matching your filters.")
else:
    cols = st.columns(3)
    for i, case in enumerate(filtered_cases):
        with cols[i % 3]:
            tags_html = "".join([f'<span class="tag {t[1]}">{t[0]}</span>' for t in case['tags']])
            st.markdown(f"""
            <div class="case-card">
                <div class="case-title">{case['title']}</div>
                <div class="case-desc">{case['desc']}</div>
                <div style="margin-bottom: 15px;">{tags_html}</div>
                <div class="time-badge">⏱ {case['time']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Start Case", key=f"btn_{i}", use_container_width=True):
                st.session_state['selected_case'] = case
                st.switch_page("pages/2_Active_Case.py")
