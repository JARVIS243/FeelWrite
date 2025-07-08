# share.py

import streamlit as st
from db import get_entry_by_date
import urllib.parse

def generate_share_url(base_url, user_id, date_str):
    params = {"uid": user_id, "date": date_str}
    return f"{base_url}?{urllib.parse.urlencode(params)}"

def show_shared_entry(user_id, date_str):
    entry = get_entry_by_date(user_id, date_str)
    if not entry:
        st.error("No diary entry found for this link.")
        return

    content, mood, tags, image_path = entry
    st.subheader(f"📅 {date_str}")
    st.write(f"**Mood:** {mood}")
    st.write(f"**Tags:** {tags}")
    st.markdown("---")
    st.text_area("📖 Entry", value=content, height=200, disabled=True)
    if image_path:
        st.image(image_path, width=300)
