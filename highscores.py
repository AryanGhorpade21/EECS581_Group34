import json 
import os

'''
Module: highscores
Description: manages loading, saving, and formatting high scores for Minesweeper game
'''

HIGHSCORE_FILE = "highscores.json" # format is a list of times in a local JSON file
MAX_SCORES = 5

def load_highscores():
    # helper function that returns a list of recorded times (in seconds)
    if not os.path.exists(HIGHSCORE_FILE):
        return []
    with open(HIGHSCORE_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_highscore(time_sec):
    # helper function that adds a new score and saves the top 5 fastest
    scores = load_highscores()
    scores.append(time_sec)
    scores = sorted(scores)[:MAX_SCORES]
    with open(HIGHSCORE_FILE, "w") as f:
        json.dump(scores, f)

def format_scores():
    # helper that returns list of formatted strings like ['1. 00:01:32', ...]
    scores = load_highscores()
    formatted = []
    for i, s in enumerate(scores, start=1):
        m, s = divmod(int(s), 60)
        h, m = divmod(m, 60)
        formatted.append(f"{i}. {h:02}:{m:02}:{s:02}")
    return formatted 
