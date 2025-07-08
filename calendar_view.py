# calendar_view.py

import pandas as pd
import streamlit as st
from db import get_all_entries, get_entry_by_date

# --- View Entry by Calendar Selection ---
def show_calendar(user_id):
    st.subheader("📆 Your Diary Activity")

    # Get all entry dates
    entries = get_all_entries(user_id)
    if not entries:
        st.info("No entries found.")
        return

    # Prepare calendar view
    df = pd.DataFrame(entries, columns=["date", "mood", "tags"])
    df["date"] = pd.to_datetime(df["date"])

    selected_date = st.date_input("Select a date to view entry:", value=df["date"].max())

    selected_str = selected_date.strftime("%Y-%m-%d")
    entry = get_entry_by_date(user_id, selected_str)

    if entry:
        content, mood, tags, image_path = entry
        st.markdown(f"### 🗓️ {selected_str}")
        st.write(f"**Mood:** {mood}")
        st.write(f"**Tags:** {tags}")
        st.markdown("---")
        st.text_area("📖 Entry Content", value=content, height=200, disabled=True)
        if image_path:
            st.image(image_path, width=300)
    else:
        st.warning("No entry found on this date.")
