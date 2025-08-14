import random
import os


DEFAULT_HECKLES = [
    "Is that the best you can do?",
    "I've seen parrots with better delivery!",
    "Try again, but with feeling this time!",
    "Even Siri speaks better than this!",
    "You're lucky this is not live on YouTube!"
]

def get_heckle():
    file_path = "heckles.txt"

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            heckles = [line.strip() for line in file if line.strip()]
        if heckles:
            return random.choice(heckles)
        else:
            print("⚠️ Heckle file is empty. Using default heckles.")
    else:
        print("⚠️ Heckle list file not found.")

    return random.choice(DEFAULT_HECKLES)
