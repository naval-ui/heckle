import speech_recognition as sr

def transcribe_audio(audio_file: str) -> str:
    """
    Transcribes spoken words from a WAV file into text using Google Speech Recognition.
    """
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            return text
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        return ""
    except Exception:
        return ""
