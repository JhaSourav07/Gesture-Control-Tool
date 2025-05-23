# Gesture Control Software 🎯🖐️

A Python-based real-time gesture control system using your webcam to simulate keyboard commands like swipe left/right — ideal for controlling videos, eBooks, or slideshows with simple hand movements.

---

## 🚀 Features

- Detects hand gestures using MediaPipe
- Simulates arrow key presses using pyautogui
- Gesture: Swipe left/right using wrist & index finger position
- Cooldown system to prevent accidental multiple triggers
- Modular codebase (organized into multiple files)

---

## 🛠️ Technologies Used

- Python 3.10 (Mandatory - else will not work)
- [MediaPipe](https://google.github.io/mediapipe/) for hand tracking
- OpenCV for webcam access & visualization
- pyautogui for simulating keyboard input

---

## 📁 Project Structure
```
Gesture Control Software
    │
    ├── main.py # Main loop for video capture and gesture logic
    ├── hand_tracker.py # Handles hand landmark detection using MediaPipe
    ├── gesture_utilities.py # Contains gesture recognition logic
    ├── README.md # This file
    └── .venv/ # (Optional) Virtual environment directory
```
---

## 🔧 Setup Instructions

1. **Clone the repository**

```
    [link here](https://github.com/JhaSourav07/Gesture-Control-Tool.git)
    cd gesture-control
```

2. **Create virtual environment (optional but recommended)**

```
    python -m venv .venv
    .venv\Scripts\activate
```

3. **Install dependencies**
```
    pip install -r requirements.txt
```

4. **Run the app**
```
    python main.py
```
---



