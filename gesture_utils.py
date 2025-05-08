import pyautogui
import time
import mediapipe as mp

mp_hands = mp.solutions.hands  # Correct way to reference MediaPipe Hands module
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8)

hand_positions = []

def detect_swipe(landmarks, current_time, last_swipe_time, cooldown=1.0, min_swipe_distance=0.2):
    global hand_positions

    # Track index finger's x position
    index_finger = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    hand_positions.append((current_time, index_finger.x))

    # Keep only recent positions (last 0.5 seconds)
    hand_positions = [pos for pos in hand_positions if current_time - pos[0] <= 0.5]

    if (current_time - last_swipe_time) < cooldown:
        return False, last_swipe_time

    # Check overall movement
    if len(hand_positions) >= 2:
        start_time, start_x = hand_positions[0]
        end_time, end_x = hand_positions[-1]
        movement_x = end_x - start_x

        if abs(movement_x) > min_swipe_distance:
            if movement_x > 0:
                pyautogui.press('right')
                print("Swipe Right")
            else:
                pyautogui.press('left')
                print("Swipe Left")
            hand_positions.clear()
            return True, current_time

    return False, last_swipe_time


def detect_play_pause(landmarks, current_time, last_gesture_time, gesture_cooldown):
    thumb_tip = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

    # Calculate distance between thumb and index finger tip
    distance = ((thumb_tip.x - index_tip.x) ** 2 + (thumb_tip.y - index_tip.y) ** 2) ** 0.5

    # Threshold to detect pinch (i.e. fingers close = "pause")
    if (current_time - last_gesture_time) > gesture_cooldown:
        if distance < 0.05:
            pyautogui.press("space")  # Usually toggles play/pause in media players
            print("Pause/Play Toggled")
            return True
    return False

           