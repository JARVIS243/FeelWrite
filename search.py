# search.py

import streamlit as st
import pandas as pd
from db import get_all_entries, get_entry_by_date

def search_entries(user_id):
    st.subheader("🔍 Search Your Entries")

    # Get all entry data
    raw_entries = get_all_entries(user_id)
    if not raw_entries:
        st.info("No diary entries found.")
        return

    df = pd.DataFrame(raw_entries, columns=["date", "mood", "tags"])
    df["date"] = pd.to_datetime(df["date"])

    keyword = st.text_input("Search by keyword")
    mood_filter = st.selectbox("Filter by mood", ["All"] + sorted(df["mood"].unique().tolist()))
    tag_filter = st.text_input("Search by tag (optional)").lower()

    results = []

    for row in df.itertuples(index=False):
        match = True
        entry_date = row.date.strftime("%Y-%m-%d")
        content_data = get_entry_by_date(user_id, entry_date)

        if content_data:
            content, mood, tags, image_path = content_data

            if keyword and keyword.lower() not in content.lower():
                match = False

            if mood_filter != "All" and row.mood != mood_filter:
                match = False

            if tag_filter and tag_filter not in row.tags.lower():
                match = False

            if match:
                results.append({
                    "date": entry_date,
                    "mood": mood,
                    "tags": tags,
                    "content": content,
                    "image": image_path
                })

    if results:
        st.success(f"Found {len(results)} matching entries:")
        for entry in results:
            st.markdown(f"### 📅 {entry['date']}")
            st.write(f"**Mood:** {entry['mood']} | **Tags:** {entry['tags']}")
            st.text_area("📖 Entry", value=entry["content"], height=150, disabled=True)
            if entry["image"]:
                st.image(entry["image"], width=300)
            st.markdown("---")
    else:
        st.warning("No matching entries found.")
