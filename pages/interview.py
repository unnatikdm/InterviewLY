import streamlit as st
import os
from moviepy.editor import VideoFileClip
from streamlit_extras.switch_page_button import switch_page

# --- Page Configuration ---
st.set_page_config(page_title="InterviewLY", page_icon="🎥", layout="wide")

# Initialize session state
if "uploaded_video_path" not in st.session_state:
    st.session_state.uploaded_video_path = None

# --- Custom Styling ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #1B1F3B, #162447);
        font-family: 'Poppins', sans-serif;
        color: white;
        text-align: center;
    }
    .title {
        font-size: 60px;
        font-weight: bold;
        color: #38BDF8;
        text-shadow: 2px 2px 10px #38BDF8;
    }
    .sidebar-title {
        font-size: 24px;
        font-weight: bold;
        color: #FF4B4B;
    }
    .upload-container {
        margin-top: 20px;
        padding: 15px;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.1);
    }
    .feature-card {
        padding: 20px;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.1);
        margin: 10px 0;
    }
    .footer {
        margin-top: 50px;
        font-size: 14px;
        color: #888;
    }
    /* Custom Button Styling */
    .stButton button {
        background: linear-gradient(135deg, #6EE7B7, #3B82F6);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 25px;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton button:hover {
        background: linear-gradient(135deg, #3B82F6, #6EE7B7);
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
    }
    .stButton button:active {
        transform: translateY(0);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    /* Analysis Buttons Grid */
    .analysis-buttons {
        display: flex;
        justify-content: space-between;
        gap: 10px;
        margin-top: 20px;
    }
    .analysis-buttons button {
        flex: 1;
        background: linear-gradient(135deg, #FF9A9E, #FAD0C4);
        color: white;
        border: none;
        padding: 15px;
        border-radius: 10px;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .analysis-buttons button:hover {
        background: linear-gradient(135deg, #FAD0C4, #FF9A9E);
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
    }
    .analysis-buttons button:active {
        transform: translateY(0);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# --- Page Title ---
st.markdown('<h1 class="title">🎥 AI-Powered Interview</h1>', unsafe_allow_html=True)

# --- Introduction Section ---
st.markdown("""
    <div style="text-align: left; margin: 20px 0;">
        <h2>Welcome to InterviewLY!</h2>
        <p>InterviewLY is your ultimate AI-powered interview assistant. Upload your interview video, and let our advanced AI analyze your performance across various metrics.</p>
    </div>
""", unsafe_allow_html=True)

# --- Features Section ---

# --- Key Features Section ---
st.markdown("## 🌟 Key Features")

# Split into 5 columns
col1, col2, col3, col4, col5 = st.columns(5)

# Column 1: Sentiment Analysis
with col1:
    st.markdown("""
        <div class="feature-card">
            <h3>🧠 Sentiment Analysis</h3>
            <p>Understand the emotional tone of your responses.</p>
        </div>
    """, unsafe_allow_html=True)

# Column 2: Eye Contact
with col2:
    st.markdown("""
        <div class="feature-card">
            <h3>👁️ Eye Contact Analysis</h3>
            <p>Evaluate your eye contact during the interview.</p>
        </div>
    """, unsafe_allow_html=True)

# Column 3: Posture Analysis
with col3:
    st.markdown("""
        <div class="feature-card">
            <h3>👨🏻‍💼 Posture Analysis</h3>
            <p>Analyze your posture and body language.</p>
        </div>
    """, unsafe_allow_html=True)

# Column 4: Gesture Analysis
with col4:
    st.markdown("""
        <div class="feature-card">
            <h3>🖐️ Gesture Analysis</h3>
            <p>Assess your hand gestures and movements.</p>
        </div>
    """, unsafe_allow_html=True)

# Column 5: Emotion Detection
with col5:
    st.markdown("""
        <div class="feature-card">
            <h3>🥹 Emotion Detection</h3>
            <p>Detect and analyze your facial expressions.</p>
        </div>
    """, unsafe_allow_html=True)
# --- Video Upload Section ---
st.markdown('<div class="upload-container">', unsafe_allow_html=True)
st.subheader("📂 Upload an MP4 Video")
uploaded_video = st.file_uploader("Drag and drop your MP4 file here", type=["mp4"], help="Limit 200MB per file. Supported formats: MP4, MPEG4")

if uploaded_video is not None:
    upload_dir = "uploaded_videos"
    os.makedirs(upload_dir, exist_ok=True)
    video_path = os.path.join(upload_dir, uploaded_video.name)
    
    with open(video_path, "wb") as f:
        f.write(uploaded_video.read())
    
    st.session_state.uploaded_video_path = video_path  # Update session state
    st.success("✅ Video uploaded successfully!")
    st.video(video_path)

st.markdown('</div>', unsafe_allow_html=True)

# --- Show Results ---
st.markdown("---")
if st.button("📊 Show Results"):
    if st.session_state.uploaded_video_path and os.path.exists(st.session_state.uploaded_video_path):
        st.session_state.show_buttons = True
    else:
        st.error("No valid video found! Upload or record first.")

if st.session_state.get("show_buttons", False):
    st.markdown("### 🛠️ Analysis Options")
    st.markdown('<div class="analysis-buttons">', unsafe_allow_html=True)
    analysis_pages = [
        ("🧠 Sentiment Analysis", "sentiment"),
        ("👁️ Eye Contact", "eyecontact"),
        ("👨🏻‍💼 Posture Analysis", "posture"),
        ("🖐️ Gesture Analysis", "gesture"),
        ("🥹 Emotion Detection", "emotion")
    ]
    for label, page in analysis_pages:
        if st.button(label):
            switch_page(analysis_page)

    st.markdown('</div>', unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
    <div class="footer">
        Made with ❤️ by InterviewLY Team | © 2025
    </div>
""", unsafe_allow_html=True)
