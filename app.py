from flask import Flask, render_template, jsonify, request
from microphone_input import start_recording, stop_recording
from speech_to_text import transcribe_audio
from speech_analysis import is_silent, analyze_and_summarize
from text_to_speech import speak
from heckle_engine import generate_feedback
import threading
import webbrowser
import traceback
import os

app = Flask(__name__, template_folder="templates", static_folder="static")

# Globals
audio_file_path = ""


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/start", methods=["POST"])
def start_session():
    try:
        start_recording()
        speak("Recording started. Speak clearly and confidently.")
        return jsonify({"message": "Recording started"}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Failed to start recording: {e}"}), 500


@app.route("/stop", methods=["POST"])
def stop_session():
    global audio_file_path

    try:
        audio_file, duration_sec = stop_recording()
        audio_file_path = audio_file
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Failed to stop recording: {e}"}), 500

    try:
        # Silence check
        if is_silent(audio_file, silence_threshold=120):
            feedback = "I couldn't hear much. Try speaking louder and closer to the mic."
            speak(feedback)
            return jsonify({
                "transcript": "",
                "feedback": feedback,
                "metrics": {}
            }), 200

        # Transcription
        transcript = transcribe_audio(audio_file)

        # Analysis + Heckle/Praise
        analysis = analyze_and_summarize(transcript, duration_sec)
        feedback = generate_feedback(analysis)

        # Speak short version
        speak(feedback)

        return jsonify({
            "transcript": transcript,
            "feedback": feedback,
            "metrics": analysis["metrics"]
        }), 200

    except Exception as e:
        traceback.print_exc()
        msg = "Something went wrong during analysis. Try again."
        speak(msg)
        return jsonify({"transcript": "", "feedback": msg, "metrics": {}}), 500
    finally:
        try:
            if os.path.exists(audio_file_path):
                os.remove(audio_file_path)
                audio_file_path = ""
        except Exception:
            pass


@app.route("/exit", methods=["POST"])
def shutdown():
    try:
        speak("Exiting. See you next time.")
    except Exception:
        pass
    func = request.environ.get("werkzeug.server.shutdown")
    if func is None:
        return jsonify({"error": "Server shutdown not available."}), 500
    try:
        func()
        return jsonify({"message": "Server shutting down..."}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")


if __name__ == "__main__":
    threading.Timer(1.0, open_browser).start()
    app.run(debug=False, use_reloader=False)
