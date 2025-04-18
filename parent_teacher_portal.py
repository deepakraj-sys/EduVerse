import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import random
from supabase import create_client, Client
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyAjKPT1ISXWdOGhVm0GyWAgOi1GFJEJHDY")

# Start a persistent chat object
chat = genai.GenerativeModel("models/gemini-1.5-flash").start_chat()

def chatbot_response_gemini(user_input):
    try:
        response = chat.send_message(user_input)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Supabase Configuration
SUPABASE_URL = "https://jsgqwqplzoqxtptnrabv.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpzZ3F3cXBsem9xeHRwdG5yYWJ2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQ3MjE1MjUsImV4cCI6MjA2MDI5NzUyNX0.n7oKI5R4fqgsHp8Ao3sL6-GY1hagJRhL-dNYvouB7Vo"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Session state initialization
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [
        {"sender": "Teacher", "message": "Hello! How can I help you today?", "time": "10:00 AM"},
        {"sender": "Parent", "message": "I'd like to discuss my child's progress in math.", "time": "10:05 AM"}
    ]

if 'scheduled_conferences' not in st.session_state:
    st.session_state.scheduled_conferences = []

def run_parent_teacher_portal():
    st.title("👨‍👩‍👧 Parent Teacher Portal")

    user_type = st.sidebar.radio("Select User Type", ["Parent", "Teacher"], key="user_type_radio")

    # ---------------- CHAT ----------------
    st.header("📬 Communication Channels")
    with st.expander("Real-time Chat"):
        messages = st.container()
        for msg in st.session_state.chat_history:
            with messages:
                col1, col2 = st.columns([2, 8])
                with col1:
                    st.markdown(f"**{msg['sender']}**")
                    st.markdown(f"*{msg['time']}*")
                with col2:
                    st.markdown(msg['message'])

        new_message = st.text_input("Type your message", key="message_input")
        if st.button("Send", key="send_btn"):
            if new_message:
                current_time = datetime.now().strftime("%I:%M %p")
                st.session_state.chat_history.append({
                    "sender": user_type,
                    "message": new_message,
                    "time": current_time
                })

                if user_type == "Parent":
                    ai_reply = chatbot_response_gemini(new_message)
                    st.session_state.chat_history.append({
                        "sender": "TeacherBot",
                        "message": ai_reply,
                        "time": datetime.now().strftime("%I:%M %p")
                    })
                st.rerun()

    # ---------------- PROGRESS ----------------
    st.header("📊 Student Progress")

    students = get_student_list()
    selected_student = st.selectbox("Select Student", students, key="student_select")

    if selected_student:
        col1, col2, col3 = st.columns(3)
        progress = get_student_progress(selected_student)
        with col1:
            st.metric("Attendance", f"{progress['attendance']}%")
        with col2:
            st.metric("Academic", f"{progress['academic']}%")
        with col3:
            st.metric("Participation", f"{progress['participation']}%")

        history = get_progress_history(selected_student)
        fig = px.line(history, x="date", y=["attendance", "academic", "participation"], title="Progress Over Time")
        st.plotly_chart(fig)

    # ---------------- CONFERENCES ----------------
    st.header("🎯 Virtual Conferences")
    available_slots = get_available_slots()
    selected_date = st.date_input("Select Date", min_value=datetime.now().date(), key="date_input")

    if selected_date:
        available_times = [slot for slot in available_slots if slot.date() == selected_date]
        if available_times:
            time_strs = [t.strftime("%I:%M %p") for t in available_times]
            selected_time = st.selectbox("Select Time", time_strs, key="time_select")
            if st.button("Schedule Conference", key="schedule_btn"):
                st.session_state.scheduled_conferences.append({
                    "user": user_type,
                    "student": selected_student,
                    "datetime": f"{selected_date} {selected_time}",
                    "meeting_link": "https://meet.google.com/jkz-iduv-uuz"
                })
                st.success("✅ Conference scheduled successfully! [Join Meeting](https://meet.google.com/jkz-iduv-uuz)")
        else:
            st.warning("No available slots on selected date.")

    # ---------------- AI INSIGHTS ----------------
    if user_type == "Teacher":
        st.header("🤖 AI Insights")
        if st.button("Generate Student Insights", key="insights_btn"):
            insights = generate_ai_insights(selected_student)
            for line in insights:
                st.markdown(f"- {line}")

    # ---------------- STUDENT MANAGEMENT ----------------
    st.header("📄 Student Management")

    if user_type == "Parent":
        with st.form("add_student_form"):
            st.subheader("Add Student Profile")
            student_name = st.text_input("Student Name")
            grade = st.text_input("Grade")
            parent_name = st.text_input("Parent Name")
            submit = st.form_submit_button("Add Student")

            if submit:
                if student_name and grade and parent_name:
                    data = {
                        "student_name": student_name,
                        "name": student_name,
                        "grade": grade,
                        "parent_name": parent_name,
                    }
                    supabase.table("students").insert(data).execute()

                    # Refresh list
                    response = supabase.table("students").select("student_name").execute()
                    students = [student['student_name'] for student in response.data]
                    st.success(f"Student '{student_name}' added successfully!")
                else:
                    st.error("Please fill out all fields!")

    elif user_type == "Teacher":
        st.subheader("All Student Profiles")
        response = supabase.table("students").select("*").execute()
        students = response.data

        if students:
            for student in students:
                st.markdown(f"**Name:** {student['student_name']}")
                st.markdown(f"Grade: {student['grade']}")
                st.markdown(f"Parent: {student['parent_name']}")

                with st.form(f"update_{student['student_name']}"):
                    attendance = st.slider("Attendance", 0, 100, 75)
                    academic = st.slider("Academic Progress", 0, 100, 80)
                    participation = st.slider("Participation", 0, 100, 70)
                    update_btn = st.form_submit_button("Update Performance")

                    if update_btn:
                        update_data = {
                            "student_name": student['student_name'],
                            "grade": student['grade'],
                            "parent_name": student['parent_name'],
                            "attendance": attendance,
                            "academic": academic,
                            "participation": participation
                        }
                        supabase.table("performance").upsert(update_data, on_conflict=["student_name", "grade"]).execute()
                        st.success(f"Updated performance for {student['student_name']}")

# ---------------- UTILITIES ----------------
def get_student_list():
    try:
        response = supabase.table("students").select("student_name").execute()
        return [student["student_name"] for student in response.data]
    except:
        return ["John Smith", "Emma Johnson", "Michael Brown"]

def get_student_progress(student):
    return {
        "attendance": random.randint(85, 100),
        "academic": random.randint(70, 100),
        "participation": random.randint(75, 100)
    }

def get_progress_history(student):
    dates = pd.date_range(start='2024-01-01', periods=10, freq='W')
    return pd.DataFrame({
        "date": dates,
        "attendance": [random.randint(85, 100) for _ in range(10)],
        "academic": [random.randint(70, 100) for _ in range(10)],
        "participation": [random.randint(75, 100) for _ in range(10)]
    })

def get_available_slots():
    now = datetime.now()
    slots = []
    for i in range(5):
        date = now.date() + timedelta(days=i)
        for hour in [9, 10, 11, 14, 15, 16]:
            slots.append(datetime.combine(date, datetime.min.time()) + timedelta(hours=hour))
    return slots

def generate_ai_insights(student):
    return [
        "Strong engagement in interactive sessions.",
        "Consistent academic performance observed.",
        "Recommended: Enhance group participation.",
        "Suggestion: Encourage creative writing tasks."
    ]

# Run the app
run_parent_teacher_portal()
