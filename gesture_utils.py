import pyautogui
import time
import mediapipe as mp
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math

mp_hands = mp.solutions.hands  # Correct way to reference MediaPipe Hands module
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8)
# Initialize system volume controller
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume_controller = cast(interface, POINTER(IAudioEndpointVolume))

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
    if (current_time - last_gesture_time) < gesture_cooldown:
        return False
    
    fingers = [
        (mp_hands.HandLandmark.THUMB_TIP, mp_hands.HandLandmark.THUMB_IP),
        (mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.INDEX_FINGER_PIP),
        (mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_PIP),
        (mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_PIP),
        (mp_hands.HandLandmark.PINKY_TIP, mp_hands.HandLandmark.PINKY_PIP),
    ]

    fingers_up = 0
    for tip,pip in fingers:
        if landmarks.landmark[tip].y < landmarks.landmark[pip].y:
            fingers_up +=1

    if fingers_up == 5 :
        pyautogui.press("space")
        print("Pause/Play triggered")
        return True


# just checking dont mind
# def control_volume(landmarks):
#     thumb_tip = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
#     index_tip = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

#     # Calculate Euclidean distance between thumb and index finger
#     dx = thumb_tip.x - index_tip.x
#     dy = thumb_tip.y - index_tip.y
#     distance = math.sqrt(dx**2 + dy**2)

#     # Map distance to volume range (0.0 to 1.0 for pycaw)
#     volume = min(max(distance * 4, 0.0), 1.0)  # Adjust 4 for sensitivity
#     volume_controller.SetMasterVolumeLevelScalar(volume, None)
#     print(f"Volume set to: {int(volume * 100)}%")           