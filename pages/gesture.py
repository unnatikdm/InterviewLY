import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import tempfile
import os
import matplotlib.pyplot as plt

# --- Initialize MediaPipe Hand Module ---
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)

# --- Page Configuration ---
st.set_page_config(page_title="Hand Gesture Detection", page_icon="✋", layout="wide")

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

# --- Function to Process Video and Detect Gestures ---
def process_video(video_path):
    """Extract frames from video and analyze hand gestures."""
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    gesture_counts = {"Open Palm": 0, "Fist": 0, "Thumbs Up": 0, "Victory": 0, "No Hand": 0}

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get landmark positions to classify gesture
            landmarks = results.multi_hand_landmarks[0].landmark
            thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP].y
            index_tip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
            pinky_tip = landmarks[mp_hands.HandLandmark.PINKY_TIP].y
            wrist = landmarks[mp_hands.HandLandmark.WRIST].y

            # Simple gesture classification
            if thumb_tip < wrist and index_tip < wrist:
                gesture = "Thumbs Up"
            elif index_tip < wrist and pinky_tip < wrist:
                gesture = "Victory"
            elif all(landmarks[i].y > wrist for i in [mp_hands.HandLandmark.THUMB_TIP,
                                                      mp_hands.HandLandmark.INDEX_FINGER_TIP,
                                                      mp_hands.HandLandmark.PINKY_TIP]):
                gesture = "Open Palm"
            elif all(landmarks[i].y < wrist for i in [mp_hands.HandLandmark.THUMB_TIP,
                                                      mp_hands.HandLandmark.INDEX_FINGER_TIP]):
                gesture = "Fist"
            else:
                gesture = "No Hand"

            gesture_counts[gesture] += 1
        else:
            gesture_counts["No Hand"] += 1

        frame_count += 1
    cap.release()

    return gesture_counts

# --- Page UI ---
st.markdown('<p class="title">✋ Hand Gesture Detection</p>', unsafe_allow_html=True)

# --- Get Video File ---
video_path = st.session_state.get("uploaded_video_path", "output.avi")

if not os.path.exists(video_path):
    st.error("⚠️ No video found! Please record or upload a video in the Interview Page.")
else:
    st.video(video_path)
    st.write("Processing... This may take a few seconds.")

    # Process Video
    gesture_distribution = process_video(video_path)

    # --- Display Gesture Report ---
    st.success("✅ Gesture Analysis Complete!")
    st.markdown(f"### **🖐️ Most Common Gesture: `{max(gesture_distribution, key=gesture_distribution.get)}`**")

    # --- Row 1: Graph and Gesture Breakdown ---
    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        # --- Display Pie Chart ---
        st.markdown("### 📊 Gesture Distribution")
        plt.figure(figsize=(6, 6))
        plt.pie(
            gesture_distribution.values(),
            labels=gesture_distribution.keys(),
            autopct='%1.1f%%',
            colors=["#ff9999", "#66b3ff", "#99ff99", "#ffcc99", "#c2c2f0"]
        )
        plt.title("Hand Gesture Distribution")
        st.pyplot(plt)

    with row1_col2:
        # --- Display Gesture Breakdown ---
        st.markdown("### 📝 Gesture Breakdown")
        for gesture, count in gesture_distribution.items():
            st.markdown(f"""
                <div class="analysis-card">
                    <h3>{gesture}</h3>
                    <p>{count} frames</p>
                </div>
            """, unsafe_allow_html=True)

    # --- Row 2: Gesture Analysis Conditions and Improvement Tips ---
    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        # --- Gesture Analysis Conditions ---
        st.markdown("### 🧠 Gesture Analysis Conditions")
        st.markdown("""
            <div class="analysis-card">
                <h3>🖐️ Open Palm</h3>
                <p>Detected when all fingers are extended and visible.</p>
            </div>
            <div class="analysis-card">
                <h3>✊ Fist</h3>
                <p>Detected when fingers are curled into a fist.</p>
            </div>
            <div class="analysis-card">
                <h3>👍 Thumbs Up</h3>
                <p>Detected when the thumb is extended upward.</p>
            </div>
            <div class="analysis-card">
                <h3>✌️ Victory</h3>
                <p>Detected when the index and middle fingers are extended.</p>
            </div>
            <div class="analysis-card">
                <h3>🚫 No Hand</h3>
                <p>Detected when no hand is visible in the frame.</p>
            </div>
        """, unsafe_allow_html=True)

    with row2_col2:
        # --- Improvement Tips ---
        st.markdown("### 🎯 Improvement Tips")
        most_common_gesture = max(gesture_distribution, key=gesture_distribution.get)
        if most_common_gesture == "Open Palm":
            st.success("""
                **Great Job!**  
                - Maintain open and confident gestures.  
                - Use open palms to emphasize points.  
                - Avoid overusing the same gesture.
            """)
        elif most_common_gesture == "Fist":
            st.warning("""
                **Moderate Gesture Usage:**  
                - Use fists sparingly to avoid appearing aggressive.  
                - Combine with open palms for balanced gestures.  
                - Practice varied hand movements.
            """)
        elif most_common_gesture == "Thumbs Up":
            st.success("""
                **Positive Gesture!**  
                - Use thumbs up to show approval or agreement.  
                - Avoid overusing to maintain impact.  
                - Combine with other gestures for variety.
            """)
        elif most_common_gesture == "Victory":
            st.success("""
                **Positive Gesture!**  
                - Use victory signs to express success or positivity.  
                - Avoid overusing to maintain impact.  
                - Combine with other gestures for variety.
            """)
        else:
            st.error("""
                **Needs Improvement:**  
                - Ensure hands are visible in the frame.  
                - Practice using gestures to enhance communication.  
                - Avoid keeping hands hidden or still.
            """)

# --- Back Button ---
st.markdown("---")
if st.button("⬅️ Back to Interview Page"):
    st.switch_page("pages/interview.py")