import speech_recognition as sr

def transcribe_audio(audio_file=r"C:\Users\bhaga\OneDrive\Desktop\AI_PublicSpeaking_Heckler\input.wav"):
    """
    Transcribes spoken words from a WAV file into text using Google Speech Recognition.

    Args:
        audio_file (str): Path to the WAV audio file.

    Returns:
        str: Transcribed text from the audio.
    """
    print("recognize2")
    
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            print("recognize1")
            text = recognizer.recognize_google(audio_data)
            return text
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand what you said."
    except sr.RequestError as e:
        return f"Could not request results from Google Speech Recognition service; {e}"
    except Exception as e:
        return f"Error: {e}"

# print(transcribe_audio())