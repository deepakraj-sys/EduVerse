import streamlit as st
import sqlite3
import hashlib
import os
import subprocess
from datetime import datetime
from PIL import Image
import pyttsx3

st.markdown("""
<style>
/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(to bottom, #2c2f36, #1e1f23);
    padding-top: 30px;
    color: #ffffff;
}
section[data-testid="stSidebar"] .css-1v3fvcr {
    font-size: 16px;
    color: #ffffff;
}
section[data-testid="stSidebar"] .css-1d391kg {
    background-color: transparent;
    color: white;
}

/* Sidebar select box and labels */
section[data-testid="stSidebar"] label, 
section[data-testid="stSidebar"] .stSelectbox > div {
    color: white !important;
}

/* Button hover */
div.stButton > button:hover {
    background-color: #198754;
    color: white;
    transition: 0.3s;
}

/* Animations */
@keyframes fadein {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
div[data-testid="stVerticalBlock"] {
    animation: fadein 0.5s ease-in;
}
</style>
""", unsafe_allow_html=True)

# === TTS ===
def speak_registration_info(language="en"):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    try:
        if language == "en":
            engine.setProperty('voice', voices[1].id)
            text = "Registration and Sign In are important to personalize your learning experience, track your progress, and ensure secure access to your data."
        elif language == "ta":
            engine.setProperty('voice', voices[0].id)
            text = "பதிவு செய்தல் மற்றும் உள்நுழைவு உங்கள் கற்றல் அனுபவத்தை தனிப்பயனாக்கும், முன்னேற்றத்தை கண்காணிக்கும் மற்றும் தரவின் பாதுகாப்பை உறுதி செய்யும்."
        else:
            text = "Language not supported."
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        st.error(f"TTS error: {e}")

# === DB SETUP ===
conn = sqlite3.connect('users.db', check_same_thread=False)
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        name TEXT,
        email TEXT,
        password TEXT,
        photo_path TEXT,
        age INTEGER,
        phone TEXT,
        dob TEXT,
        location TEXT,
        created_at TEXT
    )
''')
conn.commit()

# === UTILS ===
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def save_profile_pic(uploaded_file, username):
    os.makedirs("profile_pics", exist_ok=True)
    file_path = f"profile_pics/{username}.png"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def register_user(data):
    c.execute('''INSERT INTO users (username, name, email, password, photo_path, age, phone, dob, location, created_at) 
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
        data["username"], data["name"], data["email"], hash_password(data["password"]),
        data["photo_path"], data["age"], data["phone"], data["dob"], data["location"],
        str(datetime.now())
    ))
    conn.commit()

def login_user(username, password):
    c.execute("SELECT * FROM users WHERE username=? AND password=?", 
              (username, hash_password(password)))
    return c.fetchone()

def get_user_profile(username):
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    return c.fetchone()

# === SESSION ===
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# === PROFILE PAGE ===
def profile_page():
    st.title("👤 User Profile")
    profile = get_user_profile(st.session_state.username)

    if profile:
        st.markdown("""
        <style>
            .profile-card {
                background: linear-gradient(120deg, #f8f9fa, #ffffff);
                padding: 20px;
                border-radius: 16px;
                box-shadow: 0px 0px 15px rgba(0,0,0,0.05);
                transition: all 0.3s ease-in-out;
            }
            .profile-pic {
                border-radius: 50%;
                width: 150px;
                height: 150px;
                object-fit: cover;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            }
        </style>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(profile[4], use_column_width=False, width=150)
        with col2:
            st.markdown(f"<div class='profile-card'><h3>{profile[1]}</h3>", unsafe_allow_html=True)
            st.markdown(f"**Username:** {profile[0]}")
            st.markdown(f"**Email:** {profile[2]}")
            st.markdown(f"**Phone:** {profile[6]}")
            st.markdown(f"**Age:** {profile[5]}")
            st.markdown(f"**DOB:** {profile[7]}")
            st.markdown(f"**Location:** {profile[8]}")
            st.markdown(f"**Joined On:** {profile[9]}</div>", unsafe_allow_html=True)

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.success("Logged out successfully")
        st.rerun()

# === MAIN APP ===
def main():
    st.title("🚀 EduVerse AI Learning")
    menu = ["Home", "Login", "Register"]
    choice = st.sidebar.selectbox("📁 Navigation", menu)

    if choice == "Home":
        st.subheader("🏠 Welcome to EduVerse")
        st.markdown("EduVerse is your personalized modular learning universe powered by AI and accessibility.")
        if st.button("🔍 View App"):
            subprocess.Popen(["streamlit", "run", "streamlit_app.py"])
            st.success("Launching the main EduVerse app...")

    elif choice == "Login":
        st.subheader("🔐 Login")
        if st.button("🔊 Why Login? (English)"):
            speak_registration_info("en")
        if st.button("🔊 ஏன் உள்நுழைவு அவசியம்? (Tamil)"):
            speak_registration_info("ta")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            user = login_user(username, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome back {username}!")
                st.rerun()
            else:
                st.error("Invalid credentials")

    elif choice == "Register":
        st.subheader("📝 Register")
        if st.button("🔊 Why Register? (English)"):
            speak_registration_info("en")
        if st.button("🔊 ஏன் பதிவு அவசியம்? (Tamil)"):
            speak_registration_info("ta")

        username = st.text_input("Username")
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        photo = st.file_uploader("Upload Profile Photo", type=["png", "jpg", "jpeg"])
        age = st.number_input("Age", min_value=10, max_value=100)
        phone = st.text_input("Phone Number")
        dob = st.date_input("Date of Birth")
        location = st.text_input("Location")

        if st.button("Create Account"):
            if password != confirm_password:
                st.warning("Passwords do not match")
            elif not photo:
                st.warning("Upload a profile photo")
            else:
                try:
                    photo_path = save_profile_pic(photo, username)
                    register_user({
                        "username": username,
                        "name": name,
                        "email": email,
                        "password": password,
                        "photo_path": photo_path,
                        "age": age,
                        "phone": phone,
                        "dob": dob.strftime('%Y-%m-%d'),
                        "location": location
                    })
                    st.success("Account created! Please login.")
                except Exception as e:
                    st.error(f"Error: {e}")

# === RUN ===
if st.session_state.logged_in:
    profile_page()
else:
    main()