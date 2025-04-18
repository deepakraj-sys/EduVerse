"""BioDesign Studio - Crowdsourced Biomedical Innovation Challenge Hub"""
import streamlit as st
import time
from datetime import datetime
import random
from typing import List, Dict

def run_biodesign_studio():
    st.title("🔬 BioDesign Studio")
    st.subheader("Crowdsourced Biomedical Innovation Hub")

    # Navigation
    section = st.sidebar.radio(
        "Navigation",
        ["Challenges", "My Projects", "Team Hub", "Mentor Connect", "Submissions"]
    )

    if section == "Challenges":
        display_challenges()
    elif section == "My Projects":
        display_projects()
    elif section == "Team Hub":
        display_team_hub()
    elif section == "Mentor Connect":
        display_mentor_connect()
    elif section == "Submissions":
        display_submissions()

def display_challenges():
    """Display available biomedical challenges."""
    st.header("Current Challenges")
    
    challenges = [
        {
            "title": "Portable Dialysis Device",
            "organization": "City General Hospital",
            "deadline": "2024-03-01",
            "prize": "$5000",
            "description": "Design a portable, cost-effective dialysis device for home use."
        },
        {
            "title": "Smart Prosthetic Hand",
            "organization": "BioTech Innovations",
            "deadline": "2024-04-15",
            "prize": "Summer Internship",
            "description": "Develop an affordable, AI-powered prosthetic hand."
        }
    ]

    for idx, challenge in enumerate(challenges):
        with st.expander(f"🏆 {challenge['title']}"):
            st.write(f"**Organization:** {challenge['organization']}")
            st.write(f"**Deadline:** {challenge['deadline']}")
            st.write(f"**Prize:** {challenge['prize']}")
            st.write(f"**Description:** {challenge['description']}")
            
            if st.button(f"Join Challenge", key=f"join_{idx}"):
                st.success("Challenge joined! Head to My Projects to start working.")

def display_projects():
    """Display user's active projects."""
    st.header("My Projects")
    
    if "projects" not in st.session_state:
        st.session_state.projects = []
    
    # Create new project
    with st.expander("➕ Create New Project"):
        project_name = st.text_input("Project Name")
        project_desc = st.text_area("Project Description")
        project_team = st.multiselect("Team Members", ["Alice", "Bob", "Charlie"])
        
        if st.button("Create Project"):
            if project_name:
                new_project = {
                    "name": project_name,
                    "description": project_desc,
                    "team": project_team,
                    "progress": 0,
                    "created_at": datetime.now().strftime("%Y-%m-%d")
                }
                st.session_state.projects.append(new_project)
                st.success("Project created successfully!")
            else:
                st.warning("Project name is required.")

    # Display existing projects
    for idx, project in enumerate(st.session_state.projects):
        with st.expander(f"📋 {project['name']}"):
            st.write(f"**Created:** {project['created_at']}")
            st.write(f"**Team:** {', '.join(project['team'])}")
            st.write(f"**Description:** {project['description']}")
            
            # Progress tracking
            progress = st.slider("Project Progress", 0, 100, project['progress'], key=f"progress_{idx}")
            project['progress'] = progress
            
            # Milestones
            st.write("### Milestones")
            st.checkbox("Research Phase", value=progress >= 25, key=f"milestone1_{idx}")
            st.checkbox("Prototype Design", value=progress >= 50, key=f"milestone2_{idx}")
            st.checkbox("Initial Testing", value=progress >= 75, key=f"milestone3_{idx}")
            st.checkbox("Final Documentation", value=progress >= 100, key=f"milestone4_{idx}")

def display_team_hub():
    """Display team collaboration features."""
    st.header("Team Hub")
    
    # Team chat simulation
    st.subheader("Team Chat")
    message = st.text_input("Type your message...", key="chat_input")
    if st.button("Send", key="chat_send"):
        st.info(f"You: {message}")
        time.sleep(1)
        st.success("Alice: Thanks for the update!")

    # File sharing
    st.subheader("Shared Files")
    uploaded_file = st.file_uploader("Upload project files", key="file_upload")
    if uploaded_file:
        st.success(f"File uploaded: {uploaded_file.name}")

def display_mentor_connect():
    """Display mentor matching system."""
    st.header("Mentor Connect")
    
    mentors = [
        {
            "name": "Dr. Sarah Chen",
            "specialty": "Biomedical Devices",
            "experience": "15 years",
            "availability": "2 hours/week"
        },
        {
            "name": "Prof. James Wilson",
            "specialty": "Medical Imaging",
            "experience": "20 years",
            "availability": "1 hour/week"
        }
    ]

    for idx, mentor in enumerate(mentors):
        with st.expander(f"👨‍🏫 {mentor['name']}"):
            st.write(f"**Specialty:** {mentor['specialty']}")
            st.write(f"**Experience:** {mentor['experience']}")
            st.write(f"**Availability:** {mentor['availability']}")
            
            if st.button(f"Request Mentorship", key=f"mentor_{idx}"):
                st.success("Mentorship request sent!")

def display_submissions():
    """Display project submissions and evaluation."""
    st.header("Project Submissions")
    
    # Submit project
    with st.expander("📤 Submit Project"):
        projects = st.session_state.get('projects', [])
        if not projects:
            st.warning("No projects available to submit.")
            return

        project_select = st.selectbox("Select Project", [p['name'] for p in projects])
        submission_desc = st.text_area("Submission Description")
        uploaded_files = st.file_uploader("Upload Documentation", accept_multiple_files=True, key="submission_upload")
        
        if st.button("Submit Project"):
            st.success("Project submitted successfully!")
            st.balloons()
