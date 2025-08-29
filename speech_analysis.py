import numpy as np
import wave
from textblob import TextBlob
from heckle_engine import get_supportive_or_snark

FILLERS = {"uh", "um", "like", "you know", "basically", "actually", "so", "well"}
KEYWORD_TIPS = {
    "ai": "Great topic. Add a concrete example or story to make it relatable.",
    "data": "Numbers land better with context—compare against a baseline.",
    "vision": "A vision is stronger with a next step. What should we do first?",
    "team": "Call out a specific teammate story to make it memorable.",
    "problem": "State the problem in one sentence, then your solution in one sentence."
}

def is_silent(wav_file, silence_threshold=120):
    with wave.open(wav_file, 'rb') as wf:
        n_frames = wf.getnframes()
        audio_data = wf.readframes(n_frames)
        audio_array = np.frombuffer(audio_data, dtype=np.int16)
        if audio_array.size == 0:
            return True
        rms = np.sqrt(np.mean(audio_array.astype(np.float64)**2))
        return rms < silence_threshold

def _wpm(word_count: int, duration_sec: float) -> float:
    minutes = max(0.01, duration_sec / 60.0)
    return word_count / minutes

def analyze_and_summarize(transcript: str, duration_sec: float):
    t = (transcript or "").strip()
    word_count = len(t.split()) if t else 0
    wpm = _wpm(word_count, duration_sec)

    sentiment = TextBlob(t).sentiment.polarity if t else 0.0
    lower_words = [w.strip(".,!?;:").lower() for w in t.split()]
    filler_hits = sum(1 for w in lower_words if w in FILLERS)

    # Keyword-based tips
    tips = []
    lw_join = " ".join(lower_words)
    for k, tip in KEYWORD_TIPS.items():
        if k in lw_join:
            tips.append(tip)

    # Core guidance
    guidance = []
    if wpm > 165:
        guidance.append("Slow down a bit; aim for 120–160 words per minute.")
    elif wpm < 90 and word_count > 10:
        guidance.append("Pick up the pace slightly; aim for ~120–160 WPM.")

    if filler_hits >= 3:
        guidance.append("Reduce filler words like 'um' and 'like'—pause instead.")
    if 0 < word_count < 12:
        guidance.append("Try forming complete sentences; one clear point beats fragments.")
    if sentiment < -0.2:
        guidance.append("Mind your tone; try to keep the phrasing a touch more positive.")

    # Outcome: supportive if overall good, otherwise constructive+light snark if user wants that flavor
    overall_good = (120 <= wpm <= 160) and (filler_hits <= 1) and (sentiment >= -0.1) and (word_count >= 20)

    if overall_good:
        headline = "🎉 Great job! Clear delivery and solid pacing."
        tail = "Keep this energy—you're stage-ready."
        tone_line = "Congratulations! You are the best!"
        supportive = f"{headline} {tail}"
        final_feedback = supportive
        tts_summary = "Great job. Clear and confident!"
    else:
        snark = get_supportive_or_snark(prefer_support=True)  # keep it student-friendly
        pieces = ["Here’s how to level up:"]
        pieces.extend(guidance or ["Focus on one strong point and land it clearly."])
        if tips:
            pieces.append("Topic tips: " + " ".join(tips))
        final_feedback = f"{snark} " + " ".join(pieces)
        tts_summary = "I have a few suggestions. " + " ".join(guidance[:2] or ["Be clearer and reduce fillers."])

    return {
        "feedback_text": final_feedback,
        "tts_summary": tts_summary,
        "metrics": {
            "word_count": word_count,
            "wpm": round(wpm, 1),
            "filler_words": filler_hits,
            "sentiment": round(sentiment, 3),
        }
    }
