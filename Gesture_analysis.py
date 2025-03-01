import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
cap = cv2.VideoCapture("/content/WhatsApp Video 2025-03-01 at 2.12.16 PM(1).mp4")

total_frames = 0
gesture_frames = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    total_frames += 1
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        gesture_frames += 1

cap.release()

# Calculate percentage
gesture_percentage = (gesture_frames / total_frames) * 100 if total_frames > 0 else 0

print(f"Total Frames: {total_frames}")
print(f"Total Gesture Frames: {gesture_frames}")
print(f"Gesture Percentage: {gesture_percentage:.2f}%")
