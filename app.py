import streamlit as st
from datetime import date
from auth import create_user_table, signup_user, login_user, is_logged_in, logout_user
from db import create_tables, add_entry, update_entry, get_entry_by_date
from quotes import get_daily_quote
from utils import clean_tags, get_mood_options, make_safe_filename, format_entry_for_output
from export import export_to_txt, export_to_pdf
from calendar_view import show_calendar
from search import search_entries
from share import generate_share_url, show_shared_entry
import os

# --- Page Setup ---
st.set_page_config(
    page_title="FeelWrite",
    page_icon="assets/logo.png",  # <-- update this line
    layout="centered"
)
create_user_table()
create_tables()

# --- Custom Styles ---
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(to bottom right, #243180, #ffe8ec) !important;
    }
    .main > div {
        background: rgba(255, 255, 255, 0.9) !important;
        padding: 2rem !important;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    .title {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1.5rem;
        color: #283593;
    }
    .quote {
        background: #f0f8ff;
        padding: 15px;
        border-left: 5px solid #5c6bc0;
        font-style: italic;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        color: #333;
    }
    section[data-testid="stSidebar"] {
        background: linear-gradient(to bottom, #73b0de, #f0f4ff) !important;
        border-right: 2px solid #e0e0e0;
    }
    </style>
""", unsafe_allow_html=True)

# --- Shared View for Public Link ---
query_params = st.query_params
if "uid" in query_params and "date" in query_params:
    st.markdown("## 🌐 Shared Diary Entry")
    uid = int(query_params["uid"])
    date_str = query_params["date"]
    show_shared_entry(uid, date_str)
    st.stop()

# --- App Title ---
st.markdown('<div class="title">📝 FeelWrite – Smart Diary</div>', unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center; font-size: 16px; color: #24282b; margin-top: -10px; margin-bottom: 30px;'>
        <i>“Machane Evide Enthellum Onnu Ezhuthiyittu Poyi Koode 🥸”</i>
    </div>
""", unsafe_allow_html=True)

# --- Auth Section ---
if not is_logged_in():
    st.markdown("### 🔐 Access Your Smart Diary")
    form_type = st.radio("Choose an option:", ["Login", "Signup"], horizontal=True)

    with st.form("auth_form"):
        st.markdown("---")
        if form_type == "Signup":
            st.subheader("🚀 Create a New Account")
            name = st.text_input("👤 Full Name")
            username = st.text_input("🆔 Username")
            password = st.text_input("🔒 Password", type="password")
            submit = st.form_submit_button("✅ Sign Up")
            if submit:
                if signup_user(name, username, password):
                    st.success("Kutta Poyi Login Cheyitho ✌🏻")
                else:
                    st.error("Mone Njan Ethu Nerathe Kanda Peralle. Ethu Evide Pattula 🤨")
        else:
            st.subheader("🔑 Login to Continue")
            username = st.text_input("🆔 Username")
            password = st.text_input("🔒 Password", type="password")
            submit = st.form_submit_button("🔓 Login")
            if submit:
                user = login_user(username, password)
                if user:
                    st.session_state["user"] = user
                    st.success(f"Welcome, {user['name']} 👋")
                    st.rerun()
                else:
                    st.error("Entha Mone Ni Engane Thettikkune 😅")

# --- Main Dashboard ---
else:
    user = st.session_state["user"]
    st.success(f"Hi, {user['name']} 👋")

    # Sidebar Tools
    st.sidebar.title("📚 Tools")
    menu = st.sidebar.radio("Choose a feature:", [
        "✍ Diary",
        "📄 Export Entry",
        "🔗 Share Entry",
        "🗓 Calendar View",
        "🔍 Search"
    ])

    # Bottom-fixed Logout Button
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)
    if st.sidebar.button("🚪 Logout", key="logout_main"):
        logout_user()
        st.rerun()

    # Daily Motivation
    quote = get_daily_quote()
    if quote:
        st.markdown("### 🌟 Daily Motivation")
        st.markdown(f"<div class='quote'>{quote}</div>", unsafe_allow_html=True)

    # Diary Entry
    if menu == "✍ Diary":
        st.markdown("### 📔 Write Your Diary")
        entry_date = st.date_input("🗓️ Entry Date", value=date.today())
        entry_date_str = entry_date.strftime("%Y-%m-%d")
        existing = get_entry_by_date(user["id"], entry_date_str)

        content = ""
        mood = "Neutral"
        tags = ""
        image_path = None

        if existing:
            content, mood, tags, image_path = existing

        diary_text = st.text_area("📝 Your Thoughts", value=content, height=200, placeholder="Start writing your thoughts here...")
        mood = st.selectbox("🎭 Your Mood", get_mood_options(), index=get_mood_options().index(mood))
        tags_input = st.text_input("🏷️ Tags (comma-separated)", value=tags)
        tags = clean_tags(tags_input)

        uploaded_image = st.file_uploader("📷 Upload an image of the memorable day", type=["jpg", "jpeg", "png"])
        if uploaded_image:
            filename = make_safe_filename(f"{user['username']}_{entry_date_str}.jpg")
            img_path = f"assets/uploads/{filename}"
            with open(img_path, "wb") as f:
                f.write(uploaded_image.getbuffer())
            image_path = img_path
            st.image(image_path, width=250)

        if st.button("💾 Save Entry"):
            if existing:
                update_entry(user["id"], entry_date_str, diary_text, mood, tags, image_path)
                st.success("✏️ Entry updated.")
            else:
                add_entry(user["id"], entry_date_str, diary_text, mood, tags, image_path)
                st.success("✅ Entry saved.")

    # Export Entry
    elif menu == "📄 Export Entry":
        st.markdown("### 📄 Export Your Entry")
        entry_date = st.date_input("🗓️ Export Date", value=date.today())
        entry_date_str = entry_date.strftime("%Y-%m-%d")
        existing = get_entry_by_date(user["id"], entry_date_str)

        if not existing:
            st.warning("⚠️ No entry found for this date.")
        else:
            content, mood, tags, image_path = existing
            content_out = format_entry_for_output(entry_date_str, mood, tags, content)

            if st.button("📄 Export as TXT"):
                txt_path = f"assets/uploads/{user['username']}_{entry_date_str}.txt"
                export_to_txt(txt_path, content_out)
                st.download_button("📥 Download TXT", data=open(txt_path, "rb"), file_name=os.path.basename(txt_path))

            if st.button("🧾 Export as PDF"):
                pdf_path = f"assets/uploads/{user['username']}_{entry_date_str}.pdf"
                export_to_pdf(pdf_path, content_out)
                st.download_button("📥 Download PDF", data=open(pdf_path, "rb"), file_name=os.path.basename(pdf_path))

    # Share Entry
    elif menu == "🔗 Share Entry":
        st.markdown("### 🌐 Share Entry (Read-Only)")
        entry_date = st.date_input("🗓 Share Date", value=date.today())
        entry_date_str = entry_date.strftime("%Y-%m-%d")
        base_url = "https://feelwrite.streamlit.app"  # Replace with your hosted URL

        if get_entry_by_date(user["id"], entry_date_str):
            if st.button("🔗 Generate Share Link"):
                share_url = generate_share_url(base_url, user["id"], entry_date_str)
                st.markdown(f"<div class='share-link'>{share_url}</div>", unsafe_allow_html=True)
        else:
            st.warning("⚠️ No entry to share for this date.")

    # Calendar View
    elif menu == "🗓 Calendar View":
        st.markdown("### 🗓 Calendar")
        show_calendar(user["id"])

    # Search Entries
    elif menu == "🔍 Search":
        st.markdown("### 🔍 Search Diary")
        search_entries(user["id"])

st.markdown("<div style='text-align:center; color:#666; margin-top: 30px;'>© 2025 | Published by Aju Krishna</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
