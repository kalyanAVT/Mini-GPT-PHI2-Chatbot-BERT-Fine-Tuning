import pyttsx3

# Initialize a new engine every time for safety
def speak(text):
    if not text.strip():
        return
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 170)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except RuntimeError as e:
        if "run loop already started" in str(e):
            # Suppress the error silently
            pass
        else:
            raise e

def stop():
    try:
        engine = pyttsx3.init()
        engine.stop()
    except Exception:
        pass
