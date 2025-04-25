import streamlit as st
import random
from PIL import Image, ImageDraw
import datetime


st.markdown("""
        <style>
        .big-title { font-size: 50px !important; font-weight: 800; text-align: center; color: #6C63FF; }
        .subtext { font-size: 18px; text-align: center; color: #555; margin-bottom: 30px; }
        .button { font-size: 18px; background-color: #6C63FF; color: white; padding: 10px; border-radius: 5px; }
        </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='big-title'>🌿 Advanced To-Do List</div>", unsafe_allow_html=True)
st.markdown("<div class='subtext'>Organize your tasks with relaxation, priority, and subject management.</div>", unsafe_allow_html=True)

    # ----------------- INIT SESSION STATE ------------------
if "tasks" not in st.session_state:
        st.session_state.tasks = []

if "selected_activities" not in st.session_state:
        st.session_state.selected_activities = []

    # ----------------- HELPER FUNCTIONS ------------------

def draw_relaxing_pattern():
        width, height = 800, 400
        image = Image.new("RGB", (width, height), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)
        for _ in range(10):
            x1, y1 = random.randint(0, width), random.randint(0, height)
            x2, y2 = random.randint(0, width), random.randint(0, height)
            draw.line(
                [x1, y1, x2, y2],
                fill=(random.randint(100, 200), random.randint(150, 220), random.randint(100, 200)),
                width=3
            )
        return image

def add_task(task_name, task_description, due_date, priority, subject):
        task = {
            "name": task_name,
            "description": task_description,
            "due_date": due_date,
            "priority": priority,
            "subject": subject,
            "completed": False
        }
        st.session_state.tasks.append(task)

def toggle_task_completion(task_index):
        st.session_state.tasks[task_index]["completed"] = not st.session_state.tasks[task_index]["completed"]

def render_tasks():
        for i, task in enumerate(st.session_state.tasks):
            cols = st.columns([4, 1])
            with cols[0]:
                st.markdown(f"**{task['name']}** - _{task['subject']}_")
                st.markdown(f"📅 Due: {task['due_date']} | ⭐ Priority: {task['priority']}")
                st.markdown(f"📝 {task['description']}")
            with cols[1]:
                toggle_label = "✅" if task['completed'] else "❌"
                if st.button(f"{toggle_label}", key=f"toggle_{i}"):
                    toggle_task_completion(i)
                    st.experimental_rerun()
            st.markdown("---")

    # ----------------- SIDEBAR ------------------
st.sidebar.header("Task Management")
input_type = st.sidebar.radio("Select Input Type", ["Task Information", "Subject Management", "Activities"])

    # ----------------- TASK INFORMATION ------------------
if input_type == "Task Information":
        st.header("🖌️ Calming Drawing Screen")
        st.image(draw_relaxing_pattern(), use_column_width=True)

        st.header("📝 Add Task")
        task_name = st.text_input("Task Name")
        task_description = st.text_area("Task Description")
        due_date = st.date_input("Due Date", datetime.date.today())
        priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        subject = st.text_input("Subject")

        if st.button("Add Task"):
            add_task(task_name, task_description, due_date, priority, subject)
            st.success("✅ Task added!")

    # ----------------- SUBJECT MANAGEMENT ------------------
elif input_type == "Subject Management":
        st.header("📚 Manage Subjects")
        subject_name = st.text_input("Enter a subject name")
        if st.button("Add Subject"):
            st.success(f"📘 Subject '{subject_name}' added.")

    # ----------------- SIMULATED DRAG-AND-DROP ACTIVITIES ------------------
elif input_type == "Activities":
        st.header("🎯 Select Daily Activities")

        all_activities = [
            "Bathing", "Eating", "Studying", "Watching Movies", "Exercise", "Reading", "Sleeping", "Cooking",
            "Cleaning", "Shopping", "Meeting Friends", "Work", "Jogging", "Relaxing", "Writing", "Painting",
            "Meditating", "Traveling", "Watching TV", "Socializing", "Gaming"
        ]

        available = [a for a in all_activities if a not in st.session_state.selected_activities]

        left, right = st.columns(2)
        with left:
            st.subheader("📦 Available Activities")
            selected_to_add = st.multiselect("Pick to Add ➡️", available, key="add_list")
        with right:
            st.subheader("🎒 Selected Activities")
            selected_to_remove = st.multiselect("⬅️ Pick to Remove", st.session_state.selected_activities, key="remove_list")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("➕ Add Selected"):
                for item in selected_to_add:
                    if item not in st.session_state.selected_activities:
                        st.session_state.selected_activities.append(item)
        with col2:
            if st.button("➖ Remove Selected"):
                for item in selected_to_remove:
                    if item in st.session_state.selected_activities:
                        st.session_state.selected_activities.remove(item)

        if st.session_state.selected_activities:
            st.markdown("### ✅ Final Activity Plan:")
            for act in st.session_state.selected_activities:
                st.markdown(f"- {act}")

    # ----------------- TASK DISPLAY ------------------
if st.session_state.tasks:
        st.subheader("📋 Task List")
        render_tasks()
