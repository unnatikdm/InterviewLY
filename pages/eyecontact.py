import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import tempfile
import os
import matplotlib.pyplot as plt

# --- Initialize MediaPipe Face Mesh ---
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5)

# --- Page Configuration ---
st.set_page_config(page_title="Eye Contact Detection", page_icon="👀", layout="wide")

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

# --- Function to Process Video and Detect Eye Contact ---
def process_video(video_path):
    """Extract frames from video and analyze eye contact."""
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    eye_contact_frames = 0
    total_frames = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert frame to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(frame_rgb)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Get eye landmarks
                left_eye = [33, 133]  # Left eye inner & outer corners
                right_eye = [362, 263]  # Right eye inner & outer corners
                nose = 1  # Nose tip (used for center reference)

                left_eye_x = (face_landmarks.landmark[left_eye[0]].x + face_landmarks.landmark[left_eye[1]].x) / 2
                right_eye_x = (face_landmarks.landmark[right_eye[0]].x + face_landmarks.landmark[right_eye[1]].x) / 2
                nose_x = face_landmarks.landmark[nose].x

                # Check if eyes are centered (looking straight at camera)
                if abs(left_eye_x - nose_x) < 0.05 and abs(right_eye_x - nose_x) < 0.05:
                    eye_contact_frames += 1  # Eye contact maintained

        total_frames += 1
    cap.release()

    # Calculate Eye Contact Score (as a percentage)
    eye_contact_score = (eye_contact_frames / total_frames) * 100 if total_frames > 0 else 0
    return eye_contact_score, eye_contact_frames, total_frames

# --- Page UI ---
st.markdown('<p class="title">👀 Eye Contact Detection</p>', unsafe_allow_html=True)

# --- Get Video File ---
video_path = st.session_state.get("uploaded_video_path", "output.avi")

if not os.path.exists(video_path):
    st.error("⚠️ No video found! Please record or upload a video in the Interview Page.")
else:
    st.video(video_path)
    st.write("Processing... This may take a few seconds.")

    # Process Video
    eye_contact_score, eye_contact_frames, total_frames = process_video(video_path)

    # --- Display Eye Contact Report ---
    st.success("✅ Eye Contact Analysis Complete!")
    st.markdown(f"### **🎯 Eye Contact Score: `{eye_contact_score:.2f}%`**")
    
    # --- Row 1: Graph and Eye Contact Breakdown ---
    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        # --- Display Pie Chart ---
        st.markdown("### 📊 Eye Contact Distribution")
        labels = ['Eye Contact Maintained', 'No Eye Contact']
        values = [eye_contact_frames, total_frames - eye_contact_frames]
        colors = ['#66b3ff', '#ff9999']

        plt.figure(figsize=(6, 6))
        plt.pie(values, labels=labels, autopct='%1.1f%%', colors=colors)
        plt.title("Eye Contact Distribution")
        st.pyplot(plt)

    with row1_col2:
        # --- Display Eye Contact Breakdown ---
        st.markdown("### 📝 Eye Contact Breakdown")
        st.markdown(f"""
            <div class="analysis-card">
                <h3>Frames with Eye Contact</h3>
                <p>{eye_contact_frames}</p>
            </div>
            <div class="analysis-card">
                <h3>Total Frames Analyzed</h3>
                <p>{total_frames}</p>
            </div>
        """, unsafe_allow_html=True)

    # --- Row 2: Eye Contact Analysis Conditions and Improvement Tips ---
    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        # --- Eye Contact Analysis Conditions ---
        st.markdown("### 🧠 Eye Contact Analysis Conditions")
        st.markdown("""
            <div class="analysis-card">
                <h3>👀 Eye Contact Maintained</h3>
                <p>Detected when the eyes are centered and looking straight at the camera.</p>
            </div>
            <div class="analysis-card">
                <h3>🚫 No Eye Contact</h3>
                <p>Detected when the eyes are not centered or looking away from the camera.</p>
            </div>
        """, unsafe_allow_html=True)

    with row2_col2:
        # --- Improvement Tips ---
        st.markdown("### 🎯 Improvement Tips")
        if eye_contact_score >= 80:
            st.success("""
                **Great Job!**  
                - Maintain consistent eye contact.  
                - Practice looking directly at the camera.  
                - Avoid looking away or down frequently.
            """)
        elif eye_contact_score >= 50:
            st.warning("""
                **Moderate Eye Contact:**  
                - Practice maintaining eye contact for longer periods.  
                - Use a mirror to practice looking straight ahead.  
                - Avoid distractions that cause you to look away.
            """)
        else:
            st.error("""
                **Needs Improvement:**  
                - Focus on looking directly at the camera.  
                - Practice with a friend or in front of a mirror.  
                - Record yourself to identify areas for improvement.
            """)
