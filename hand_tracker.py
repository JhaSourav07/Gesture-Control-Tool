import cv2
import mediapipe as mp

# Initialize MediaPipe Hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8)

def get_hand_landmarks(frame):
    # Convert the frame to RGB as MediaPipe requires RGB format
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the frame to get landmarks
    results = hands.process(frame_rgb)
    
    if results.multi_hand_landmarks:  # If hand landmarks are detected
        return results.multi_hand_landmarks[0]  # Return the first detected hand
    
    return None  # No hand detected
