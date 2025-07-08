# utils.py

import re

# --- Mood Options ---
def get_mood_options():
    return ["Happy", "Sad", "Excited", "Anxious", "Neutral", "Tired", "Grateful", "Angry", "Hopeful", "Calm"]

# --- Clean Tags ---
def clean_tags(tag_string):
    """
    Convert comma-separated tag input to a clean, lowercase list.
    e.g. "Mood, Reflection ,growth" => "mood,reflection,growth"
    """
    tags = [tag.strip().lower() for tag in tag_string.split(",") if tag.strip()]
    return ",".join(tags)

# --- Sanitize File Name ---
def make_safe_filename(text):
    """
    Converts a string (like username or date) into a safe filename.
    """
    return re.sub(r'[^\w\-_.]', '_', text)

# --- Format Entry (for export/share) ---
def format_entry_for_output(date, mood, tags, content):
    return f"""Date: {date}
Mood: {mood}
Tags: {tags}

--- Entry ---
{content}
"""
