import cv2
import dlib

# Load face detector and landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("/content/shape_predictor_68_face_landmarks.dat")

cap = cv2.VideoCapture("/content/WhatsApp Video 2025-03-01 at 2.12.16 PM(1).mp4")

total_frames = 0
eye_contact_frames = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    total_frames += 1  # Count total frames
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    if len(faces) > 0:  # If at least one face is detected
        eye_contact_frames += 1

cap.release()

# Calculate percentage
eye_contact_percentage = (eye_contact_frames / total_frames) * 100
print(f"Eye Contact Percentage: {eye_contact_percentage:.2f}%")
