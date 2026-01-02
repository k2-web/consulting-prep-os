import streamlit as st
import datetime
import random
import pandas as pd

class SessionManager:
    """
    Manages user sessions and simulates a backend database.
    """
    
    @staticmethod
    def init_session():
        """Initialize session state variables if they don't exist."""
        # Robust Reset for Tanvi
        if 'user_identity' not in st.session_state or st.session_state['user_identity'] != 'Tanvi':
            st.session_state.clear()
            st.session_state['user_identity'] = 'Tanvi'
            
        defaults = {
            'user_xp': 0,
            'cases_completed': 0,
            'hours_practiced': 0.0,
            'average_score': 0,
            'completed_modules': [],
            'interview_history': [],
            'performance_trend': [], 
            'skills': {
                'Problem Structuring': 0,
                'Quantitative Analysis': 0,
                'Business Acumen': 0,
                'Communication': 0,
                'Synthesis': 0
            }
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value

    @staticmethod
    def add_xp(amount):
        """Add XP to the user's profile."""
        st.session_state['user_xp'] += amount
        # st.toast(f"🚀 +{amount} XP Gained!")

    @staticmethod
    def mark_module_complete(module_name):
        """Mark a learning module as complete."""
        if module_name not in st.session_state['completed_modules']:
            st.session_state['completed_modules'].append(module_name)
            SessionManager.add_xp(50)

    @staticmethod
    def save_interview(case_name, feedback, score=None):
        """Save an interview session result."""
        if score is None:
            score = random.randint(70, 95)
            
        entry = {
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "case": case_name,
            "feedback": feedback,
            "score": score
        }
        st.session_state['interview_history'].append(entry)
        st.session_state['cases_completed'] += 1
        st.session_state['hours_practiced'] += 0.5 # Assume 30 mins per case
        
        # Update average score
        current_avg = st.session_state['average_score']
        count = st.session_state['cases_completed']
        new_avg = ((current_avg * (count - 1)) + score) / count
        st.session_state['average_score'] = int(new_avg)
        
        # Update trend
        st.session_state['performance_trend'].append(score)
        if len(st.session_state['performance_trend']) > 10:
            st.session_state['performance_trend'].pop(0)
            
        SessionManager.add_xp(100)

    @staticmethod
    def get_stats():
        """Return user statistics."""
        return {
            "xp": st.session_state.get('user_xp', 0),
            "cases_completed": st.session_state.get('cases_completed', 0),
            "hours_practiced": st.session_state.get('hours_practiced', 0),
            "average_score": st.session_state.get('average_score', 0),
            "trend": st.session_state.get('performance_trend', []),
            "skills": st.session_state.get('skills', {})
        }
