import cv2
import pyautogui
import time
from hand_tracker import get_hand_landmarks  # Import hand tracking logic
from gesture_utils import detect_swipe, detect_play_pause    
import mediapipe as mp
import voice_command

mp_hands = mp.solutions.hands  # Correct way to reference MediaPipe Hands module
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8)

# Variables to track swipe gestures
last_swipe_time = 0  # Time tracking for swipe cooldown
swipe_cooldown = 1  # Cooldown time in seconds for valid swipe detection
last_gesture_time = 0
gesture_cooldown = 1.5

cap = cv2.VideoCapture(0)  # Open webcam


while True:
    ret, frame = cap.read()  # Read frame from webcam
    frame = cv2.flip(frame, 1)

    if not ret:
        break
    
    # Get hand landmarks using the 'get_hand_landmarks' function
    landmarks = get_hand_landmarks(frame)
    
    if voice_command.gesture_active and landmarks:
        current_time = time.time() 

        # Call the function to detect swipe gestures
        swiped, last_swipe_time = detect_swipe(landmarks, current_time, last_swipe_time)
        # last_swipe_time = current_time  # Update the last swipe time

        if swiped:
            continue
        

        if detect_play_pause(landmarks, current_time, last_gesture_time, gesture_cooldown):
            last_gesture_time = current_time
            continue
        
        # just checking dont mind
        # if (current_time - last_gesture_time) > gesture_cooldown:
        #     control_volume(landmarks)
        #     last_gesture_time = current_time
        #     continue
        
    # Show the processed frame
    cv2.imshow('Hand Gesture Recognition', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
        break

cap.release()  # Release the camera
cv2.destroyAllWindows()  # Close all OpenCV windows
