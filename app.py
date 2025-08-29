from flask import Flask, render_template, jsonify, request
from microphone_input import start_recording, stop_recording
from speech_to_text import transcribe_audio
from speech_analysis import is_silent, analyze_and_summarize
from text_to_speech import speak
import threading
import webbrowser
import traceback
import os

app = Flask(__name__, template_folder="templates", static_folder="static")

# ===== Routes =====

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
    """
    Stop recording, transcribe, analyze, and generate feedback.
    """
    try:
        audio_file, duration_sec = stop_recording()
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Failed to stop recording: {e}"}), 500

    try:
        # 1) Silence check (fast)
        try:
            if is_silent(audio_file, silence_threshold=120):
                transcript = ""
                feedback = "I couldn't hear much. Try speaking closer to the mic with steady volume."
                speak(feedback)
                return jsonify({
                    "transcript": transcript,
                    "feedback": feedback
                }), 200
        except Exception:
            # Continue even if the silence check fails
            pass

        # 2) Transcribe recorded audio
        transcript = transcribe_audio(audio_file)

        # 3) Analyze transcript + generate constructive feedback
        analysis = analyze_and_summarize(
            transcript=transcript,
            duration_sec=max(1.0, duration_sec)  # guard divide-by-zero
        )
        feedback = analysis["feedback_text"]

        # 4) Speak a SHORT version so it feels snappy
        speak(analysis["tts_summary"])

        return jsonify({
            "transcript": transcript,
            "feedback": feedback,
            "metrics": analysis["metrics"]
        }), 200

    except Exception as e:
        traceback.print_exc()
        msg = "Something went wrong during analysis. Try again."
        speak(msg)
        return jsonify({"transcript": "", "feedback": msg}), 500
    finally:
        # optional: clean temp wav after processing
        try:
            if os.path.exists(audio_file):
                os.remove(audio_file)
        except Exception:
            pass

@app.route("/exit", methods=["POST"])
def shutdown():
    """
    Gracefully shut down Flask without throwing socket errors on Windows.
    """
    # speak first (engine may block)
    try:
        speak("Exiting. See you next time.")
    except Exception:
        pass

    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        # Not running with the Werkzeug server (e.g., in prod)
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
    # Opening the browser in a timer is fine; to avoid WinError 10038 during shutdown:
    # 1) avoid the reloader threads
    # 2) don't kill sockets from other threads while select() is polling
    threading.Timer(1.0, open_browser).start()
    app.run(debug=False, use_reloader=False)  # <- important on Windows
