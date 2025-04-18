import streamlit as st
import random

def run_edu_quests():
    st.title("🎯 EduQuests")
    st.subheader("Embark on Educational Adventures")

    # Quest Categories
    quest_categories = {
        "Science Explorer": ["Lab Safety Quest", "Chemical Reactions Challenge", "Physics Phenomena Hunt"],
        "Math Master": ["Geometry Journey", "Algebra Adventure", "Statistics Safari"],
        "Literature Legend": ["Poetry Path", "Story Structure Quest", "Character Analysis Challenge"]
    }

    # Select category
    category = st.selectbox("Choose your Quest Category", list(quest_categories.keys()))

    def safety_quiz():
        st.markdown("### 🛡️ Safety Check Before You Begin")
        q1 = st.radio("1. What should you wear during a lab experiment?", ["Sunglasses", "Goggles and Gloves", "Hat"])
        q2 = st.radio("2. What should you do if something spills?", ["Ignore it", "Tell a teacher", "Wipe it with your sleeve"])
        passed = q1 == "Goggles and Gloves" and q2 == "Tell a teacher"
        if passed:
            st.success("✅ You passed the safety check! Begin your quest.")
        else:
            st.error("❌ Please review the safety instructions and try again.")
        return passed

    st.write("### Available Quests")
    for quest in quest_categories[category]:
        with st.expander(quest):
            st.write("**Objective:** Complete challenges to earn points and badges")
            st.write("**Rewards:** Knowledge points, digital badges, achievement certificates")

            # Safety quiz gate
            if st.button(f"Take Safety Quiz for {quest}", key=f"quiz_{quest}"):
                if safety_quiz():
                    st.session_state[f"{quest}_ready"] = True

            if st.session_state.get(f"{quest}_ready", False):
                progress = random.randint(0, 100)
                st.progress(progress / 100)
                st.write(f"Progress: {progress}%")
                if st.button(f"Start {quest}", key=quest):
                    st.success("Quest started! Your adventure begins...")
                    st.balloons()

    # Leaderboard
    st.sidebar.write("### Quest Leaderboard")
    leaderboard = {"Alex": 2500, "Maya": 2300, "Sam": 2100, "Leo": 1900, "Zoe": 1800}
    for player, score in leaderboard.items():
        st.sidebar.write(f"{player}: {score} points")

    # ------------------- LABS -------------------
    st.write("## 🧪 Interactive Lab Simulators")

    if category == "Science Explorer":
        st.write("### 🔬 Real-time Science Lab Simulation")
        lab_running = st.checkbox("Run real-time simulation")
        if lab_running:
            st.success("🔁 Live updates enabled: You’re simulating in real-time!")
            st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Science_symbols.svg/800px-Science_symbols.svg.png", width=150)
            st.markdown("**Observation:** The chemical reaction begins to release gas 💨.\n\n**Timer:** 3s... 2s... 1s... BOOM! 🌡️")

        if st.button("Generate Random Experiment"):
            experiment = random.choice(["Volcano Eruption", "Liquid Density Test", "Magnetism Map"])
            st.info(f"🧪 Run: **{experiment}**")
            st.code(f'POST /api/simulation/start/{{"{experiment.lower().replace(" ", "_")}"}}')

    elif category == "Math Master":
        st.write("### 📐 Real-time Math Visualization")
        st.components.v1.iframe("https://www.geogebra.org/material/iframe/id/ggbmathtools/width/700/height/500", height=500)

        if st.button("Run Simulation: Graph Update"):
            st.success("✅ Plotting function: y = sin(x) + cos(x)")
            st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Sine_and_Cosine.svg/512px-Sine_and_Cosine.svg.png", width=400)

        st.components.v1.iframe("https://www.desmos.com/calculator", height=500)

    elif category == "Literature Legend":
        st.write("### 📖 Storytelling Animation")
        st.markdown("""
        <svg height="100" width="500">
          <text x="0" y="50" fill="purple" font-size="24" font-family="Verdana">
            ✨ Writing your journey...
            <animate attributeName="x" from="0" to="250" dur="6s" repeatCount="indefinite" />
          </text>
        </svg>
        """, unsafe_allow_html=True)

    # ------------------- Safety Instructions -------------------
    st.write("## 🚨 Lab/Class Safety Instructions")

    if category == "Science Explorer":
        st.markdown("""
        ### 🧪 Science Lab Safety
        - Wear goggles and gloves 🧤
        - Know where safety exits are 🚪
        - Never eat/drink in the lab
        """)

    elif category == "Math Master":
        st.markdown("""
        ### 📏 Math Lab Safety
        - Use geometric tools properly 📐
        - Keep your area tidy 🧹
        - Take breaks during long sessions ⏱️
        """)

    elif category == "Literature Legend":
        st.markdown("""
        ### 📚 Literature Lab Safety
        - Avoid eye strain with regular breaks 👀
        - Keep your study materials organized 📓
        - Respect digital workspace etiquette 💻
        """)