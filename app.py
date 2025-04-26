import streamlit as st
from streamlit_extras.switch_page_button import switch_page

# --- Page Configuration ---
st.set_page_config(page_title="InterviewLY", page_icon="💼", layout="wide")

# --- Custom CSS for EXTREMELY MASSIVE TITLE ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0F172A, #1E293B);
        font-family: 'Poppins', sans-serif;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100vh;
        text-align: center;
    }
    .content-container {
        width: 100%;
        max-width: 1200px;
        margin: auto;
        padding: 20px;
    }
    .header-title {
        font-size: 250px;
        font-weight: 1000;
        color: #38BDF8;
        text-transform: uppercase;
        letter-spacing: 6px;
        text-shadow: 0px 0px 50px rgba(56, 189, 248, 1);
        margin-bottom: 20px;
    }
    .header-subtitle {
        font-size: 32px;
        max-width: 900px;
        color: #CBD5E1;
        margin: 20px auto;
    }
    .stButton > button {
        background: linear-gradient(90deg, #38BDF8, #6366F1);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 20px 50px;
        font-size: 30px;
        font-weight: 900;
        cursor: pointer;
        transition: all 0.3s ease-in-out;
        box-shadow: 0px 10px 30px rgba(99, 102, 241, 0.8);
        margin-top: 40px;
    }
    .stButton > button:hover {
        transform: scale(1.2);
        box-shadow: 0px 15px 40px rgba(99, 102, 241, 1);
    }
    .analysis-card {
        padding: 20px;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.1);
        margin: 10px;
        transition: all 0.3s ease;
    }
    .analysis-card:hover {
        transform: translateY(-5px);
        box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.2);
    }
    .footer {
        margin-top: 50px;
        font-size: 14px;
        color: #888;
    }
    </style>
""", unsafe_allow_html=True)

# --- Main Section ---
st.markdown('<div class="content-container">', unsafe_allow_html=True)

# --- HUGE HUGE TITLE ---
st.markdown('<p class="header-title">InterviewLY</p>', unsafe_allow_html=True)

# --- Start Interview Button (NAVIGATE TO INTERVIEW PAGE) ---

if st.button("🎤 START INTERVIEW"):
    switch_page("interview.py")

# --- Analysis Conditions Section (ROW 1 WITH DIFFERENT COLUMNS) ---
st.markdown("## 🧠 Analysis Conditions")
col1, col2, col3, col4, col5 = st.columns(5)  # Split into 5 columns

with col1:
    st.markdown("""
        <div class="analysis-card">
            <h3>🎯 Confidence Score</h3>
            <p>Measures your confidence level based on your posture, eye contact, and speech clarity.</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="analysis-card">
            <h3>🗣️ Speech Analysis</h3>
            <p>Analyzes your speech for clarity, tone, and filler words to improve communication.</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="analysis-card">
            <h3>👀 Eye Contact</h3>
            <p>Evaluates your eye contact to ensure you are engaging with the interviewer.</p>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
        <div class="analysis-card">
            <h3>🖐️ Gesture Analysis</h3>
            <p>Assesses your hand gestures to ensure they are natural and supportive of your speech.</p>
        </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown("""
        <div class="analysis-card">
            <h3>😊 Emotion Detection</h3>
            <p>Detects your facial expressions to ensure you are conveying the right emotions.</p>
        </div>
    """, unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
    <div class="footer">
        Made with ❤️ by InterviewLY Team | © 2025
    </div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
