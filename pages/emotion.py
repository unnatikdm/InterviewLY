import streamlit as st
import cv2
import os
import tempfile
import numpy as np
import matplotlib.pyplot as plt
from deepface import DeepFace
from concurrent.futures import ThreadPoolExecutor

# --- Page Configuration ---
st.set_page_config(page_title="Emotion Detection", page_icon="😊", layout="wide")

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
    .upload-container {
        margin-top: 20px;
        padding: 15px;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.1);
    }
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
    .analysis-card {
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
    </style>
""", unsafe_allow_html=True)

# --- Extract Frames from Video ---
def extract_frames(video_path, frame_rate=5):
    """Extracts frames from the video at a given frame rate."""
    temp_dir = tempfile.mkdtemp()
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        st.error(f"⚠️ Error opening video file: {video_path}. Please check the path and try again.")
        return []

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_interval = max(1, fps // frame_rate)
    frame_count = 0
    saved_frames = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % frame_interval == 0:
            frame_path = os.path.join(temp_dir, f"frame_{frame_count}.jpg")
            cv2.imwrite(frame_path, frame)
            saved_frames.append(frame_path)
        frame_count += 1

    cap.release()
    return saved_frames

# --- Detect Emotions ---
def analyze_frame(frame):
    """Detects emotions in a single frame using DeepFace."""
    try:
        analysis = DeepFace.analyze(frame, actions=["emotion"], enforce_detection=False)
        dominant_emotion = analysis[0]["dominant_emotion"]
        return dominant_emotion
    except Exception as e:
        st.warning(f"⚠️ Error analyzing frame: {e}")
        return "No Face Detected"

def analyze_emotions_parallel(frames):
    """Runs emotion detection in parallel for faster speed."""
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(analyze_frame, frames))
    return results

# --- Generate Emotion Distribution Report ---
def generate_emotion_report(emotions):
    """Generates and displays emotion distribution report."""
    emotion_counts = {emotion: emotions.count(emotion) for emotion in set(emotions)}
    sorted_emotions = sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True)

    if sorted_emotions:
        dominant_emotion, count = sorted_emotions[0]
        st.markdown(f"### **😊 Dominant Emotion: `{dominant_emotion.upper()}`**")

        # --- Display Emotion Distribution as a Pie Chart ---
        plt.figure(figsize=(6, 6))
        plt.pie(
            emotion_counts.values(), 
            labels=emotion_counts.keys(), 
            autopct='%1.1f%%', 
            colors=["#ff9999","#66b3ff","#99ff99","#ffcc99","#c2c2f0","#ffb3e6"]
        )
        plt.title("Emotion Distribution")
        st.pyplot(plt)

        # --- Display Distribution Details ---
        st.markdown("**📊 Emotion Breakdown:**")
        for emotion, count in sorted_emotions:
            st.markdown(f"""
                <div class="analysis-card">
                    <h3>{emotion.capitalize()}</h3>
                    <p>{count} frames</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.error("⚠️ No emotions detected! Ensure faces are visible in the video.")

# --- Page Title ---
st.markdown('<p class="title">🎭 Emotion Detection</p>', unsafe_allow_html=True)

# --- Get the last recorded/uploaded video ---
# First try session state
video_path = st.session_state.get("uploaded_video_path", "uploaded_videos/converted-video.mp4")


# Debugging: Print the video path and check if it exists
st.write(f"Video Path: {video_path}")
st.write(f"File exists: {os.path.exists(video_path)}")

# Check if the video path exists
if not os.path.exists(video_path):
    st.error("⚠️ No video found! Please record or upload a video in the Interview Page.")
else:
    st.video(video_path)
    st.write("Processing... This may take a few seconds.")

    # Extract Frames & Analyze Emotions
    frames = extract_frames(video_path, frame_rate=5)
    if frames:
        emotions = analyze_emotions_parallel(frames)
        st.success("✅ Emotion Analysis Complete!")

        # --- Row 1: Graph and Emotion Breakdown ---
        row1_col1, row1_col2 = st.columns(2)

        with row1_col1:
            # --- Display Pie Chart ---
            st.markdown("### 📊 Emotion Distribution")
            plt.figure(figsize=(6, 6))
            plt.pie(
                [emotions.count(emotion) for emotion in set(emotions)],
                labels=set(emotions),
                autopct='%1.1f%%',
                colors=["#ff9999","#66b3ff","#99ff99","#ffcc99","#c2c2f0","#ffb3e6"]
            )
            plt.title("Emotion Distribution")
            st.pyplot(plt)

        with row1_col2:
            # --- Display Emotion Breakdown ---
            st.markdown("### 📝 Emotion Breakdown")
            for emotion, count in {emotion: emotions.count(emotion) for emotion in set(emotions)}.items():
                st.markdown(f"""
                    <div class="analysis-card">
                        <h3>{emotion.capitalize()}</h3>
                        <p>{count} frames</p>
                    </div>
                """, unsafe_allow_html=True)

        # --- Row 2: Emotion Analysis Conditions and Improvement Tips ---
        row2_col1, row2_col2 = st.columns(2)

        with row2_col1:
            # --- Emotion Analysis Conditions ---
            st.markdown("### 🧠 Emotion Analysis Conditions")
            st.markdown("""
                <div class="analysis-card">
                    <h3>😊 Happy</h3>
                    <p>Detected when the person is smiling or showing positive facial expressions.</p>
                </div>
                <div class="analysis-card">
                    <h3>😠 Angry</h3>
                    <p>Detected when the person shows signs of frustration or anger.</p>
                </div>
                <div class="analysis-card">
                    <h3>😢 Sad</h3>
                    <p>Detected when the person shows signs of sadness or distress.</p>
                </div>
                <div class="analysis-card">
                    <h3>😲 Surprise</h3>
                    <p>Detected when the person shows signs of surprise or shock.</p>
                </div>
                <div class="analysis-card">
                    <h3>😐 Neutral</h3>
                    <p>Detected when the person shows no strong emotional expression.</p>
                </div>
                <div class="analysis-card">
                    <h3>🚫 No Face Detected</h3>
                    <p>Detected when no face is visible in the frame.</p>
                </div>
            """, unsafe_allow_html=True)

        with row2_col2:
            # --- Improvement Tips ---
            st.markdown("### 🎯 Improvement Tips")
            if "happy" in emotions:
                st.success("""
                    **Great Job!**  
                    - Maintain positive facial expressions.  
                    - Smile naturally to convey confidence.  
                    - Avoid overexaggerating expressions.
                """)
            elif "neutral" in emotions:
                st.warning("""
                    **Moderate Expressions:**  
                    - Practice showing more emotion in your expressions.  
                    - Use gestures to complement your facial expressions.  
                    - Record yourself to identify areas for improvement.
                """)
            else:
                st.error("""
                    **Needs Improvement:**  
                    - Focus on expressing emotions clearly.  
                    - Practice in front of a mirror to improve facial expressions.  
                    - Seek feedback from others to refine your expressions.
                """)


