import streamlit as st
import random
from datetime import datetime
import matplotlib.pyplot as plt
import requests

# Simulated import (for structure)
from educational_api_connector import APIConnector

OPENWEATHER_API_KEY = "3114a14ea2ac7203cd532f4cc1d4afc6"

def get_weather(city="Chennai"):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = {
            "temp": data['main']['temp'],
            "humidity": data['main']['humidity'],
            "weather_main": data['weather'][0]['main']  # e.g., Rain, Clear, Clouds
        }
        return weather
    else:
        return None

def run_ecoschool_sim():
    st.title("🌍 EcoSchool Sim")
    st.subheader("Virtual School Ecosystem Management")

    weather = get_weather()
    if weather:
        st.info(f"**Weather in Delhi**: {weather['weather_main']}, {weather['temp']} °C, Humidity: {weather['humidity']}%")
        is_sunny = weather['weather_main'] in ["Clear"]
        is_rainy = weather['weather_main'] in ["Rain", "Drizzle"]
    else:
        st.warning("Unable to fetch weather data.")
        is_sunny = False
        is_rainy = False

    if 'students' not in st.session_state:
        st.session_state.students = {}

    if 'selected_student' not in st.session_state:
        st.session_state.selected_student = None

    with st.sidebar:
        st.subheader("👩‍🏫 Student Management")
        student_names = list(st.session_state.students.keys())
        selected = st.selectbox("Select Student", ["-- New Student --"] + student_names)

        if selected == "-- New Student --":
            new_student = st.text_input("Enter new student name")
            if st.button("Add Student") and new_student:
                if new_student not in st.session_state.students:
                    st.session_state.students[new_student] = {
                        'metrics': {
                            'waste_reduction': 0,
                            'energy_efficiency': 0,
                            'water_conservation': 0,
                            'green_score': 0
                        },
                        'actions': [],
                        'history': []
                    }
                    st.session_state.selected_student = new_student
                    st.success(f"Student '{new_student}' added!")
        else:
            st.session_state.selected_student = selected

    if not st.session_state.selected_student:
        st.warning("Please select or add a student to begin.")
        return

    student = st.session_state.students[st.session_state.selected_student]
    metrics = student['metrics']

    with st.sidebar:
        st.subheader("🌱 Resource Management")
        waste_action = st.selectbox("Waste Management", ["Implement Recycling", "Composting Program", "Zero-waste Initiative"])
        energy_action = st.selectbox("Energy Conservation", ["Solar Panels", "LED Lighting", "Smart Thermostats"])
        water_action = st.selectbox("Water Conservation", ["Rain Gardens", "Low-flow Fixtures", "Greywater Systems"])

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Waste Reduction", f"{metrics['waste_reduction']}%")
    with col2:
        st.metric("Energy Efficiency", f"{metrics['energy_efficiency']}%")
    with col3:
        st.metric("Water Conservation", f"{metrics['water_conservation']}%")

    if st.button("Run Simulation"):
        waste_increase = 5 if "Recycling" in waste_action else 10 if "Composting" in waste_action else 15
        energy_increase = 15 if "Solar" in energy_action else 10 if "LED" in energy_action else 5
        water_increase = 10 if "Rain" in water_action else 5 if "Low-flow" in water_action else 15

        # Weather-based modifiers
        if is_sunny and "Solar" in energy_action:
            energy_increase += 5  # Sunny boost
        if is_rainy and "Rain" in water_action:
            water_increase += 5  # Rainwater harvesting boost

        metrics['waste_reduction'] += waste_increase
        metrics['energy_efficiency'] += energy_increase
        metrics['water_conservation'] += water_increase
        metrics['green_score'] = round(
            (metrics['waste_reduction'] + metrics['energy_efficiency'] + metrics['water_conservation']) / 3, 1
        )

        student['history'].append({
            'timestamp': datetime.now().strftime("%H:%M:%S"),
            'green_score': metrics['green_score']
        })

        st.success(f"Simulation Complete! Green Score: {metrics['green_score']}%")

    st.subheader("🏍️ Achievement Badges")
    if metrics['green_score'] >= 90:
        st.success("🥇 Eco Champion!")
    elif metrics['green_score'] >= 70:
        st.info("🥈 Eco Leader")
    elif metrics['green_score'] >= 50:
        st.warning("🥉 Eco Explorer")
    else:
        st.error("🚧 Keep Going!")

    st.subheader("📘 Log Green Actions")
    with st.form("log_green_action_form"):
        action = st.text_input("Describe your green action:")
        submitted = st.form_submit_button("Log Action")
        if submitted and action:
            student['actions'].append({
                'action': action,
                'date': datetime.now().strftime("%Y-%m-%d")
            })
            st.success("Green action logged!")

    if st.checkbox("📜 Show Green Action History"):
        st.write("### Green Action History")
        for a in student['actions']:
            st.write(f"- {a['action']} (Date: {a['date']})")

    if st.checkbox("📈 Show Green Score Progress"):
        if len(student['history']) >= 2:
            timestamps = [entry['timestamp'] for entry in student['history']]
            scores = [entry['green_score'] for entry in student['history']]
            fig, ax = plt.subplots()
            ax.plot(timestamps, scores, marker='o', linestyle='-', color='green')
            ax.set_xlabel("Time")
            ax.set_ylabel("Green Score")
            ax.set_title("Progress Over Time")
            st.pyplot(fig)
        else:
            st.info("Need at least 2 simulation runs to show progress chart.")

    st.subheader("🕍 EcoSchool Leaderboard")
    leaderboard = sorted(st.session_state.students.items(), key=lambda x: x[1]['metrics']['green_score'], reverse=True)
    for i, (name, data) in enumerate(leaderboard):
        st.write(f"{i+1}. **{name}** - 🌿 {data['metrics']['green_score']}% Green Score")