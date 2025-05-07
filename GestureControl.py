import cv2
import mediapipe as mp
import pyautogui
import time

# Initialize MediaPipe Hands and OpenCV
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8)
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

# Variables to track movement
prev_x = 0
prev_y = 0
swipe_threshold = 0.1  # Movement threshold for swipe gesture
last_swipe_time = 0  # Track the last time a swipe occurred
swipe_cooldown = 1  # Time in seconds between valid swipes


while True:
    ret, frame = cap.read()
    
    if not ret:
        break
    
    # Convert to RGB (MediaPipe requires RGB)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the frame to get hand landmarks
    results = hands.process(frame_rgb)
    
    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            # Get wrist and index finger tip positions
            wrist = landmarks.landmark[mp_hands.HandLandmark.WRIST]
            index_finger = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            
            # Calculate movement
            movement_x = wrist.x - index_finger.x
            movement_y = wrist.y - index_finger.y
            
            current_time = time.time()

            # Detect swipe gesture (horizontal swipe)
            if abs(movement_x) > swipe_threshold and (current_time - last_swipe_time) > swipe_cooldown:
                if movement_x < 0:  # Swipe left
                    pyautogui.press('left')  # Simulate left arrow key press
                    print("Swiped Left")
                elif movement_x > 0:  # Swipe right
                    pyautogui.press('right')  # Simulate right arrow key press
                    print("Swiped Right")


                last_swipe_time = current_time

                mp_draw.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)
    
    # Display the frame with hand landmarks
    cv2.imshow('Hand Gesture Recognition', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
        break

cap.release()
cv2.destroyAllWindows()
