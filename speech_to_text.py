import whisper
import speech_recognition as sr

# Load Whisper model once globally to save time on repeated calls
try:
    model = whisper.load_model("base")
except Exception as e:
    print("❌ Failed to load Whisper model:", e)
    model = None

def transcribe_audio(file_path: str) -> str:
    """
    Transcribes audio from the given file path.
    Uses Whisper first; if it fails, falls back to Google Speech Recognition.
    """
    # First attempt: Whisper
    if model:
        try:
            result = model.transcribe(file_path, language="en")
            text = result.get("text", "").strip()
            if text:
                return text
        except Exception as e:
            print("⚠ Whisper failed, falling back to Google:", e)
    
    # Fallback: Google Speech Recognition
    try:
        r = sr.Recognizer()
        with sr.AudioFile(file_path) as source:
            audio = r.record(source)
        return r.recognize_google(audio)
    except Exception as e2:
        print("❌ Both Whisper and Google failed:", e2)
        return ""
