from flask import Flask, render_template, jsonify
from microphone_input import start_recording, stop_recording
from speech_to_text import transcribe_audio
from speech_analysis import is_silent
from heckle_engine import get_random_heckle
from text_to_speech import speak
import threading
import webbrowser
import traceback
import time
from heckle_engine import get_supportive_or_snark


app = Flask(__name__, template_folder="templates", static_folder="static")
last_heckle = ""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start_session():
    global last_heckle
    try:
        speak("Recording started, please speak clearly.")

        # Step 1: Record audio (5 seconds demo)
        try:
            start_recording()
            time.sleep(5)  # record for 5 seconds
            audio_file, duration = stop_recording()
            print(f"Audio recorded to: {audio_file} (Duration: {duration:.2f}s)")
        except Exception as record_error:
            print("Error during recording:", record_error)
            raise

        # Step 2: Check if audio is silent
        try:
            if is_silent(audio_file, silence_threshold=200):
                transcript = ""
                heckle = "🦗 I can't hear anything... did you mute yourself?"
                speak(heckle)
                last_heckle = heckle
                return jsonify({"transcript": transcript, "heckle": heckle})
            print("Audio is not silent.")
        except Exception as silence_error:
            print("Error during silence check:", silence_error)
            # fallback: continue even if silence check fails

        # Step 3: Transcribe the audio
        try:
            transcript = transcribe_audio(audio_file)
            if not transcript or transcript.strip() == "":
                transcript = "🤔 Couldn't understand you!"
            print(f"Transcribed Text: {transcript}")
        except Exception as transcribe_error:
            print("Error during transcription:", transcribe_error)
            transcript = "🤔 Couldn't understand you!"

        # Step 4: Generate a heckle based on the transcript
        try:
            heckle = get_random_heckle(transcript)
            print(f"Heckle: {heckle}")
            speak(f"Heckle: {heckle}")
            last_heckle = heckle
        except Exception as heckle_error:
            print("Error generating heckle:", heckle_error)
            heckle = "🤡 Oops, my brain just tripped over its own shoelaces!"
            speak(heckle)
            last_heckle = heckle

        # Return both transcript and heckle
        return jsonify({"transcript": transcript, "heckle": heckle})
    except Exception as e:
        traceback.print_exc()
        heckle = "🤡 Oops, my brain just tripped over its own shoelaces!"
        speak(heckle)
        last_heckle = heckle
        return jsonify({"transcript": "", "heckle": heckle})

@app.route("/replay")
def replay_heckle():
    if last_heckle:
        speak(last_heckle)
    return ('', 204)

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")

if __name__ == "__main__":
    threading.Timer(1.0, open_browser).start()
    app.run(debug=True)
