import random

HECKLES = [
    "🎤 Did you just whisper to your shoes?",
    "😂 I've seen toasters with better projection!",
    "😴 Wake me up when you bring the energy!",
    "🤡 Even Siri sounds more confident!"
]

SUPPORT = [
    "👏 That was smooth! Keep up the fluency.",
    "🔥 You're sounding sharp and clear!",
    "😎 Smooth operator! Keep that rhythm going.",
    "👌 Excellent flow! Stay confident."
]

def generate_feedback(analysis: dict) -> str:
    metrics = analysis.get("metrics", {})
    wpm = metrics.get("wpm", 0)
    fillers = metrics.get("filler_words", 0)

    if fillers > 3 or wpm < 90:
        return random.choice(HECKLES)
    else:
        return random.choice(SUPPORT)
def get_random_heckle(transcript: str) -> str:
    """
    Pick a random heckle, optionally influenced by transcript.
    """
    if not transcript or transcript.strip() == "":
        return random.choice([
            "🦗 I can't hear anything... did you mute yourself?",
            "🤔 Hello? Testing… is this thing on?",
        ])
    return random.choice(HECKLES)