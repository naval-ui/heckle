import random

SUPPORTIVE = [
    "Nice start—keep your shoulders relaxed and project your voice.",
    "Good effort! A touch slower and you'll land every point.",
    "Solid energy. Add a pause after key lines for effect.",
    "You’re getting there. One strong example will make it pop.",
]

SNARK_LIGHT = [
    "Spice it up—your content deserves better delivery.",
    "I’m awake, but barely. Give me one vivid example!",
    "You’ve got the ideas—now punch them in clean sentences.",
    "Nearly there. Trim the fillers and you’ll sound pro.",
]

def get_supportive_or_snark(prefer_support=True):
    if prefer_support:
        return random.choice(SUPPORTIVE)
    return random.choice(SNARK_LIGHT)
