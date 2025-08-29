import pyttsx3

_engine = None

def _get_engine():
    global _engine
    if _engine is None:
        _engine = pyttsx3.init()
    return _engine

def speak(text):
    try:
        engine = _get_engine()
        engine.say(text)
        engine.runAndWait()
    except RuntimeError:
        pass
    except Exception as e:
        print("❌ Text-to-speech error:", e)