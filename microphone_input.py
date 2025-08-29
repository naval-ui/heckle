import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import tempfile
import time

fs = 44100
_recording_data = []
_recording_start_time = None
_is_recording = False
_stream = None

def start_recording():
    global _recording_data, _recording_start_time, _is_recording, _stream
    if _is_recording:
        return  # already recording
    _recording_data = []
    _is_recording = True
    _recording_start_time = time.time()

    def callback(indata, frames, time_info, status):
        if status:
            print(status)
        if _is_recording:
            _recording_data.append(indata.copy())

    _stream = sd.InputStream(callback=callback, channels=1, samplerate=fs)
    _stream.start()
    print("🎙 Recording started...")

def stop_recording():
    global _is_recording, _stream, _recording_start_time, _recording_data
    if not _is_recording:
        raise RuntimeError("Recording is not running.")

    _is_recording = False

    if _stream:
        _stream.stop()
        _stream.close()
        _stream = None

    duration = time.time() - (_recording_start_time or time.time())
    audio = np.concatenate(_recording_data, axis=0) if _recording_data else np.zeros((1,1))

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    wav.write(temp_file.name, fs, (audio * 32767).astype(np.int16))

    # reset
    _recording_data = []
    _recording_start_time = None

    print(f"🛑 Recording stopped. Duration: {duration:.2f}s -> {temp_file.name}")
    return temp_file.name, duration
