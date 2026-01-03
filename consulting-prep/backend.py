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
    def save_interview(case_name, feedback, score=None, breakdown=None):
        """Save an interview session result."""
        final_score = 0
        
        if isinstance(score, dict):
            # Calculate weighted average if score is a breakdown
            # Structure (30%), Analysis (40%), Communication (30%)
            s = score.get('Structure', 0)
            a = score.get('Analysis', 0)
            c = score.get('Communication', 0)
            final_score = int(s * 0.3 + a * 0.4 + c * 0.3)
            breakdown = score
        elif score is not None:
            final_score = score
            breakdown = {"Structure": score, "Analysis": score, "Communication": score}
        else:
            final_score = random.randint(70, 95)
            breakdown = {"Structure": final_score, "Analysis": final_score, "Communication": final_score}
            
        entry = {
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "case": case_name,
            "feedback": feedback,
            "score": final_score,
            "breakdown": breakdown
        }
        st.session_state['interview_history'].append(entry)
        
        # XP is still additive
        SessionManager.add_xp(100)

    @staticmethod
    def get_stats():
        """Return user statistics calculated dynamically from history."""
        history = st.session_state.get('interview_history', [])
        
        # Calculate Stats
        cases_completed = len(history)
        hours_practiced = cases_completed * 0.5 # Assume 30 mins per case
        
        if cases_completed > 0:
            avg_score = int(sum(item['score'] for item in history) / cases_completed)
            trend = [item['score'] for item in history][-10:] # Last 10
        else:
            avg_score = 0
            trend = []
            
        return {
            "xp": st.session_state.get('user_xp', 0),
            "cases_completed": cases_completed,
            "hours_practiced": hours_practiced,
            "average_score": avg_score,
            "trend": trend,
            "skills": st.session_state.get('skills', {})
        }
