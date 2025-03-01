import cv2
import mediapipe as mp

# Initialize Mediapipe Pose with the fastest settings
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, model_complexity=0)

# Load video
video_path = "/content/infosys.mp4"
cap = cv2.VideoCapture(video_path)

# Get video properties
fps = int(cap.get(cv2.CAP_PROP_FPS))  # Frames per second
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # Total frames
duration_sec = total_frames / fps  # Video duration in seconds

# **FAST FRAME SKIPPING FORMULA**
frame_skip = max(5, int(duration_sec / 200))  # Dynamically adjusts but keeps it at least 5

print(f"🎥 Video Duration: {duration_sec:.2f} sec | FPS: {fps} | Frame Skip: {frame_skip}")

frames_with_pose = 0
good_posture_frames = 0
low_score_reasons = {"Head Tilt": 0, "Shoulder Misalignment": 0, "Spine Bend": 0}
processed_frames = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    processed_frames += 1

    if processed_frames % frame_skip != 0:
        continue  # **FAST SKIPPING**

    # **Downscale Frame for Speed (smallest possible resolution)**
    frame = cv2.resize(frame, (320, 240))  
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame_rgb)

    if results.pose_landmarks:
        frames_with_pose += 1
        landmarks = results.pose_landmarks.landmark
        head_y = landmarks[mp_pose.PoseLandmark.NOSE].y
        left_shoulder_y = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y
        right_shoulder_y = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y
        spine_y = (landmarks[mp_pose.PoseLandmark.LEFT_HIP].y + landmarks[mp_pose.PoseLandmark.RIGHT_HIP].y) / 2

        score = 100

        if abs(left_shoulder_y - right_shoulder_y) > 0.12:
            score -= 20
            low_score_reasons["Shoulder Misalignment"] += 1
        
        if abs(head_y - left_shoulder_y) > 0.25:
            score -= 30
            low_score_reasons["Head Tilt"] += 1
        
        if abs(spine_y - left_shoulder_y) > 0.35:
            score -= 30
            low_score_reasons["Spine Bend"] += 1
        
        if score >= 60:
            good_posture_frames += 1

cap.release()

# Compute final posture score
if frames_with_pose == 0:
    print("❌ No frames processed. Check video file.")
else:
    posture_percentage = (good_posture_frames / frames_with_pose) * 100
    print(f"✅ Posture Score: {posture_percentage:.2f}%")
    print(f"📸 Pose detected in {frames_with_pose / processed_frames * 100:.2f}% of frames.")

    if posture_percentage < 100:
        print("📉 Reasons for low score:")
        for reason, count in low_score_reasons.items():
            if count > 0:
                percentage = (count / frames_with_pose) * 100
                print(f"- {reason}: {percentage:.2f}% of the time")
