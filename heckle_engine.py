import random

# Define the heckle function
def get_random_heckle():
    heckles = [
        "Even your echo wants to walk out.",
        "My ears want a refund.",
        "That was a plot twist... into boredom.",
        "Try again, but this time say *anything* interesting.",
        "Did you practice that in a cave?",
        "Are you charging people to listen to this?",
        "I've better die than listen to this shit.",
    ]
    return random.choice(heckles)