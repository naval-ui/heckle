from flask import Flask, render_template, jsonify
from microphone_input import record_and_reduce_noise
from speech_to_text import transcribe_audio
from speech_analysis import is_silent
from text_to_speech import speak
import threading
import webbrowser
import traceback
import random

app = Flask(__name__, template_folder="templates", static_folder="static")
last_heckle = ""
audio_file_path = ""  # global to store temporary audio path

# Heckle function
def get_random_heckle():
    heckles = [
        "Even your echo wants to walk out morron.",
        "My ears want a refund for this shit.",
        "That was a plot twist... into boredom.",
        "Try again, but this time say *anything* interesting or just pay me back blitchhhhhhh.",
        "Did you practice that in a Tilak raj chadha institute of management and technology? 🤢🤮🤮",
        "Are you charging people to listen to this garbage😂😂😂",
        "I've better die than listen to this shitttttt.",
    ]
    return random.choice(heckles)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start_session():
    global audio_file_path
    try:
        speak("Recording started, please speak clearly.")

        # Step 1: Record audio and reduce noise
        try:
            result = record_and_reduce_noise()
            if isinstance(result, tuple):
                audio_file_path = result[0]
            else:
                audio_file_path = result
            print(f"Audio recorded to: {audio_file_path}")
        except Exception as record_error:
            print("Error during recording or noise reduction:", record_error)
            raise

        # Step 2: Check if audio is silent
        try:
            if is_silent(audio_file_path, silence_threshold=200):
                transcript = ""
                # Pick a random heckle for silence
                heckle = get_random_heckle()
                print(f"Heckle for silence: {heckle}")
                speak(heckle)
                global last_heckle
                last_heckle = heckle
                return jsonify({"transcript": transcript, "heckle": heckle})
            print("Audio is not silent.")
        except Exception as silence_error:
            print("Error during silence check:", silence_error)
            # fallback: continue even if silence check fails

        # Inform frontend to call /stop for transcription
        return jsonify({"message": "Recording finished. Call /stop to transcribe and get a heckle."})

    except Exception as e:
        traceback.print_exc()
        heckle = "🤡 Oops, my brain just tripped over its own shoelaces!"
        speak(heckle)
        last_heckle = heckle
        return jsonify({"transcript": "", "heckle": heckle})

@app.route("/stop", methods=["POST"])
def stop_session():
    global last_heckle, audio_file_path
    try:
        if not audio_file_path:
            raise ValueError("No recorded audio found. Please start recording first.")

        # Step 3: Transcribe the audio
        try:
            transcript = transcribe_audio(audio_file_path)
            if not transcript or transcript.strip() == "":
                transcript = "🤔 Couldn't understand you!"
            print(f"Transcribed Text: {transcript}")
        except Exception as transcribe_error:
            print("Error during transcription:", transcribe_error)
            transcript = "🤔 Couldn't understand you!"

        # Step 4: Generate heckle
        try:
            heckle = get_random_heckle()  # No arguments needed
            print(f"Heckle: {heckle}")
            speak(f"Heckle: {heckle}")
            last_heckle = heckle
        except Exception as heckle_error:
            print("Error generating heckle:", heckle_error)
            heckle = "🤡 Oops, my brain just tripped over its own shoelaces!"
            speak(heckle)
            last_heckle = heckle

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
