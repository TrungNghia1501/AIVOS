import cv2
import mediapipe as mp
import time
import socket

# Initialize MediaPipe solutions
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Open webcam
# '0' is usually the default webcam index. Change if needed.
cap = cv2.VideoCapture(0)

# Set up the socket connection parameters
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 4013         # The port used by the server

# Use the Pose module to detect the human body
with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:

    # Distance threshold for triggering the AI.
    # This value is the ratio of the person's body height to the frame height.
    # A larger value means the person is closer.
    distance_threshold = 0.35  # Initial estimated value for a ~1-meter distance

    # Flag to track the AI's active state
    ai_active = False

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Could not read frame from webcam.")
            break

        # Flip the image horizontally for a more intuitive view
        image = cv2.flip(image, 1)
        # Convert the BGR image to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Process the image to detect the body pose
        results = pose.process(image_rgb)
        
        image.flags.writeable = True

        person_is_close = False
        
        if results.pose_landmarks:
            # Get the coordinates of key body landmarks to estimate height
            left_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
            right_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
            left_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
            right_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]

            # Calculate the relative body height using the midpoints of shoulders and hips
            shoulder_mid_y = (left_shoulder.y + right_shoulder.y) / 2
            hip_mid_y = (left_hip.y + right_hip.y) / 2
            
            person_height = abs(shoulder_mid_y - hip_mid_y)

            # Uncomment the line below to help with calibration
            # print(f"Relative person height: {person_height}")
            
            # Check if the person is closer than the defined threshold
            if person_height > distance_threshold:
                person_is_close = True
            
            # Draw the landmarks and connections on the image
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))
        
        # Logic to activate or deactivate the AI
        if person_is_close and not ai_active:
            print("Customer detected! Activating the AI receptionist...")
            ai_active = True
            try:
                # Connect to the other application and send an "activate" message
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((HOST, PORT))
                    s.sendall(b'activate')
            except ConnectionRefusedError:
                print("Connection to the AI character server failed. Is the server running?")

        elif not person_is_close and ai_active:
            print("Customer has left. Deactivating the AI receptionist...")
            ai_active = False
            try:
                # Connect to the other application and send a "deactivate" message
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((HOST, PORT))
                    s.sendall(b'deactivate')
            except ConnectionRefusedError:
                print("Connection to the AI character server failed. Is the server running?")

        # Display the AI's status on the screen
        status_text = "AI: Active" if ai_active else "AI: Inactive"
        color = (0, 255, 0) if ai_active else (0, 0, 255)
        cv2.putText(image, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)

        cv2.imshow('AI Receptionist System', image)

        # Break the loop if the 'q' key is pressed
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
