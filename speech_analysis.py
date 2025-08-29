import wave
import numpy as np
from textblob import TextBlob

def is_silent(file_path, silence_threshold=120):
    with wave.open(file_path, "rb") as wf:
        frames = wf.readframes(wf.getnframes())
        samples = np.frombuffer(frames, dtype=np.int16)
        amplitude = np.abs(samples).mean()
        return amplitude < silence_threshold

def analyze_and_summarize(transcript: str, duration_sec: float):
    words = transcript.split()
    word_count = len(words)
    wpm = (word_count / duration_sec) * 60 if duration_sec > 0 else 0
    filler_words = sum(word.lower() in ["um", "uh", "like", "you know"] for word in words)

    blob = TextBlob(transcript)
    sentiment = blob.sentiment.polarity

    metrics = {
        "word_count": word_count,
        "wpm": round(wpm, 2),
        "filler_words": filler_words,
        "sentiment": "positive" if sentiment > 0 else "negative" if sentiment < 0 else "neutral"
    }

    feedback_text = f"You spoke {word_count} words at {wpm:.1f} WPM with {filler_words} fillers."
    short_summary = f"{'Fluent' if filler_words < 3 and wpm > 100 else 'Needs practice'} speech."

    return {"feedback_text": feedback_text, "tts_summary": short_summary, "metrics": metrics}
