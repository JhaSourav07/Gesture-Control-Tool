import pyautogui
import time
import mediapipe as mp

mp_hands = mp.solutions.hands  # Correct way to reference MediaPipe Hands module
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8)

def detect_swipe(landmarks, current_time, last_swipe_time, swipe_cooldown):
    wrist = landmarks.landmark[mp_hands.HandLandmark.WRIST]  # Get wrist landmark
    index_finger = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]  # Get index finger tip landmark
    
    # Calculate horizontal movement
    movement_x = wrist.x - index_finger.x
    swipe_threshold = 0.1  # Set the threshold for swipe movement
    
    if abs(movement_x) > swipe_threshold and (current_time - last_swipe_time) > swipe_cooldown:
        # Check if the movement is left or right
        if movement_x < 0:  # Swipe left
            pyautogui.press('left')  # Simulate left arrow key press
            print("Swiped Left")
        elif movement_x > 0:  # Swipe right
            pyautogui.press('right')  # Simulate right arrow key press
            print("Swiped Right")
        return True  # Gesture detected
    
    return False  # No gesture detected
