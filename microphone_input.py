import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import tempfile
import time

fs = 44100
_recording_data = []
_is_recording = False
_stream = None
_start_time = None


def start_recording():
    global _recording_data, _is_recording, _stream, _start_time
    if _is_recording:
        return
    _recording_data = []
    _is_recording = True
    _start_time = time.time()

    def callback(indata, frames, time_info, status):
        if status:
            print(status)
        if _is_recording:
            _recording_data.append(indata.copy())

    _stream = sd.InputStream(callback=callback, channels=1, samplerate=fs)
    _stream.start()
    print("🎙 Recording started...")


def stop_recording():
    global _is_recording, _stream, _recording_data, _start_time
    if not _is_recording:
        raise RuntimeError("Recording not active.")
    _is_recording = False
    if _stream:
        _stream.stop()
        _stream.close()
    duration = time.time() - (_start_time or time.time())
    audio = np.concatenate(_recording_data, axis=0) if _recording_data else np.zeros((1, 1))
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    wav.write(temp_file.name, fs, (audio * 32767).astype(np.int16))
    print(f"🛑 Recording stopped. Duration {duration:.2f}s -> {temp_file.name}")
    return temp_file.name, duration
