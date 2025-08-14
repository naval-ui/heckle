from textblob import TextBlob

# === Configurations ===
FILLERS = ["uh", "um", "like", "you know", "basically", "actually"]
KEYWORD_HECKLES = {
    "synergy": "Synergy? Are you in a corporate meeting?",
    "vision": "Everyone has a vision. Try glasses.",
    "AI": "Oh no, not another AI talk!"
}

def analyze_transcript(transcript, duration_minutes, speak):
    transcript_lower = transcript.lower()
    word_count = len(transcript.split())
    duration_minutes = max(duration_minutes, 0.01)  # Avoid divide by zero
    wpm = word_count / duration_minutes
    sentiment = TextBlob(transcript).sentiment.polarity
    filler_count = sum(transcript_lower.split().count(f) for f in FILLERS)

    if filler_count >= 3:
        speak("Cut the filler words! It's not a podcast.")
    if wpm > 160:
        speak("Slow down, Eminem.")
    elif wpm < 80:
        speak("Wake me up when you're done.")
    if sentiment < -0.2:
        speak("Wow, someone's in a mood.")
    elif sentiment > 0.6:
        speak("Too cheerful. Are you selling toothpaste?")
    for word, heckle in KEYWORD_HECKLES.items():
        if word in transcript_lower:
            speak(heckle)
