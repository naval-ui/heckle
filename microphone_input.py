import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import tempfile
import time

fs = 44100
recording_data = []
recording_start_time = None
is_recording = False
stream = None  # <-- Store the stream object


def start_recording():
    global recording_data, recording_start_time, is_recording, stream
    recording_data = []
    is_recording = True
    recording_start_time = time.time()

    def callback(indata, frames, time_info, status):
        if status:
            print(status)
        if is_recording:
            recording_data.append(indata.copy())

    stream = sd.InputStream(callback=callback, channels=1, samplerate=fs)
    stream.start()  # <-- Start the stream
    print("🎙 Recording started...")


def stop_recording():
    global is_recording, stream
    is_recording = False

    if stream:
        stream.stop()   # <-- Stop the stream
        stream.close()  # <-- Close the stream
        stream = None

    duration = time.time() - recording_start_time
    audio = np.concatenate(recording_data, axis=0)

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    wav.write(temp_file.name, fs, (audio * 32767).astype(np.int16))

    print(f"🛑 Recording stopped. Duration: {duration:.2f} sec")
    return temp_file.name, duration


def record_and_reduce_noise(duration=10):
    """
    Keeps compatibility for old code expecting a timed recording.
    """
    print(f"🎙 Timed recording for {duration} seconds...")
    start_recording()
    time.sleep(duration)
    return stop_recording()
