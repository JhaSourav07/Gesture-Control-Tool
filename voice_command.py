import speech_recognition as sr
import threading

gesture_active = False  # Global flag

def listen_for_commands():
    global gesture_active
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)

    while True:
        with mic as source:
            print("Listening for 'start' or 'stop'...")
            try:
                audio = recognizer.listen(source, timeout=5)
                command = recognizer.recognize_google(audio).lower()
                print(f"You said: {command}")

                if "start" in command:
                    gesture_active = True
                    print("Gesture control activated.")

                elif "stop" in command:
                    gesture_active = False
                    print("Gesture control deactivated.")

            except sr.UnknownValueError:
                print("Didn't understand, try again.")
            except sr.WaitTimeoutError:
                pass  # No speech within timeout

# Start listening in background
threading.Thread(target=listen_for_commands, daemon=True).start()
