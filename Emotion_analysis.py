import cv2
from deepface import DeepFace
from collections import Counter

def detect_emotion(frame):
    try:
        # Resize the frame for faster processing
        small_frame = cv2.resize(frame, (200, 200))  # Resize to 200x200
        result = DeepFace.analyze(small_frame, actions=['emotion'], enforce_detection=False)
        return result[0]['dominant_emotion']
    except:
        return "No Face Detected"

# Load video
cap = cv2.VideoCapture("/content/WhatsApp Video 2025-02-28 at 2.33.10 AM.mp4")

emotions_list = []
frame_skip = 5  # Process every 5th frame
frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    if frame_count % frame_skip == 0:  # Skip frames for faster processing
        emotion = detect_emotion(frame)
        emotions_list.append(emotion)
    
    frame_count += 1

cap.release()

# Count occurrences of each emotion
emotion_counts = Counter(emotions_list)

# Display final summary
print("\n🔹 **Emotion Analysis Summary** 🔹")
for emotion, count in emotion_counts.items():
    print(f"{emotion.capitalize()}: {count} times")

