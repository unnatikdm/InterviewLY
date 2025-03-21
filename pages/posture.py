import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import tempfile
import os
import matplotlib.pyplot as plt

# --- Initialize MediaPipe Pose Module ---
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# --- Page Configuration ---
st.set_page_config(page_title="Posture Analysis", page_icon="🧍‍♂️", layout="wide")

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

# --- Function to Process Video and Detect Posture ---
def process_video(video_path):
    """Extract frames from video and analyze posture."""
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    straight_posture_frames = 0
    total_frames = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert frame to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)

        if results.pose_landmarks:
            # Get landmark positions
            left_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
            right_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
            left_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
            right_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]

            # Calculate shoulder and hip alignment (posture)
            shoulder_slope = abs(left_shoulder.y - right_shoulder.y)
            hip_slope = abs(left_hip.y - right_hip.y)

            # Define threshold to classify good posture
            if shoulder_slope < 0.05 and hip_slope < 0.05:
                straight_posture_frames += 1  # Straight posture detected

        total_frames += 1
    cap.release()

    # Calculate Posture Score (as a percentage)
    posture_score = (straight_posture_frames / total_frames) * 100 if total_frames > 0 else 0
    return posture_score, straight_posture_frames, total_frames

# --- Page UI ---
st.markdown('<p class="title">🧍‍♂️ Posture Analysis</p>', unsafe_allow_html=True)

# --- Get Video File ---
video_path = st.session_state.get("uploaded_video_path", "output.avi")

if not os.path.exists(video_path):
    st.error("⚠️ No video found! Please record or upload a video in the Interview Page.")
else:
    st.video(video_path)
    st.write("Processing... This may take a few seconds.")

    # Process Video
    posture_score, straight_posture_frames, total_frames = process_video(video_path)

    # --- Display Posture Report ---
    st.success("✅ Posture Analysis Complete!")
    st.markdown(f"### **🎯 Posture Score: `{posture_score:.2f}%`**")

    # --- Row 1: Graph and Posture Breakdown ---
    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        # --- Display Pie Chart ---
        st.markdown("### 📊 Posture Distribution")
        labels = ['Straight Posture', 'Slouched Posture']
        values = [straight_posture_frames, total_frames - straight_posture_frames]
        colors = ['#66b3ff', '#ff9999']

        plt.figure(figsize=(6, 6))
        plt.pie(values, labels=labels, autopct='%1.1f%%', colors=colors)
        plt.title("Posture Distribution")
        st.pyplot(plt)

    with row1_col2:
        # --- Display Posture Breakdown ---
        st.markdown("### 📝 Posture Breakdown")
        st.markdown(f"""
            <div class="analysis-card">
                <h3>Frames with Straight Posture</h3>
                <p>{straight_posture_frames}</p>
            </div>
            <div class="analysis-card">
                <h3>Total Frames Analyzed</h3>
                <p>{total_frames}</p>
            </div>
        """, unsafe_allow_html=True)

    # --- Row 2: Posture Analysis Conditions and Improvement Tips ---
    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        # --- Posture Analysis Conditions ---
        st.markdown("### 🧠 Posture Analysis Conditions")
        st.markdown("""
            <div class="analysis-card">
                <h3>📏 Posture Alignment</h3>
                <p>Good posture is determined by the alignment of your shoulders and hips. If the slope of your shoulders and hips is less than 0.05, it is considered straight posture.</p>
            </div>
            <div class="analysis-card">
                <h3>🎯 Posture Score</h3>
                <p>The posture score is calculated as the percentage of frames with straight posture out of the total frames analyzed.</p>
            </div>
            <div class="analysis-card">
                <h3>📉 Slouched Posture</h3>
                <p>Slouched posture occurs when the slope of your shoulders or hips exceeds 0.05. This can lead to back pain and poor body language.</p>
            </div>
        """, unsafe_allow_html=True)

    with row2_col2:
        # --- Improvement Tips ---
        st.markdown("### 🎯 Improvement Tips")
        if posture_score >= 80:
            st.success("""
                **Great Job!**  
                - Maintain your current posture.  
                - Practice mindfulness to stay aware of your posture.  
                - Continue regular posture exercises.
            """)
        elif posture_score >= 50:
            st.warning("""
                **Moderate Posture:**  
                - Practice standing and sitting straight.  
                - Use ergonomic furniture to support your posture.  
                - Perform posture-correcting exercises daily.
            """)
        else:
            st.error("""
                **Needs Improvement:**  
                - Focus on aligning your shoulders and hips.  
                - Use a posture corrector if necessary.  
                - Consult a physiotherapist for personalized advice.
            """)

# --- Back Button ---
st.markdown("---")
if st.button("⬅️ Back to Interview Page"):
    st.switch_page("pages/interview.py")