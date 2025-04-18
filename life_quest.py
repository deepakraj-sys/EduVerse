
"""Life Quest module - Life skills and personal development"""
import streamlit as st

def run_life_quest():
    st.title("🌟 Life Quest")
    st.subheader("Develop Essential Life Skills")

    # Life Skills Categories
    skills = {
        "Financial Literacy": ["Budgeting Basics", "Saving Strategies", "Investment Introduction"],
        "Communication": ["Public Speaking", "Active Listening", "Digital Communication"],
        "Problem Solving": ["Critical Thinking", "Decision Making", "Creative Solutions"]
    }

    # Skill selection
    category = st.selectbox("Choose Skill Category", list(skills.keys()))
    skill = st.selectbox("Select Specific Skill", skills[category])

    # Interactive learning
    st.write("### Skill Development")
    
    # Progress tracking
    progress = {
        "Theory": 70,
        "Practice": 50,
        "Application": 30
    }

    for stage, value in progress.items():
        st.write(f"**{stage}**")
        st.progress(value/100)
        st.write(f"{value}% complete")

    # Practice exercises
    st.write("### Practice Exercise")
    st.text_area("Complete today's challenge", placeholder="Enter your response here...")
    
    if st.button("Submit Practice"):
        st.success("Great work! Keep practicing to master this skill.")
