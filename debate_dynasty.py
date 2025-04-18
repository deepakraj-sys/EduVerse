
"""Debate Dynasty module - Structured debate and argumentation learning"""
import streamlit as st

def run_debate_dynasty():
    st.title("🎭 Debate Dynasty")
    st.subheader("Master the Art of Argumentation")

    # Debate Topics
    topics = {
        "Science & Technology": [
            "Should AI development be regulated?",
            "Is space exploration worth the cost?",
            "Should genetic engineering be allowed in humans?"
        ],
        "Society & Ethics": [
            "Should social media have age restrictions?",
            "Should homework be mandatory?",
            "Should school uniforms be required?"
        ],
        "Environment": [
            "Should single-use plastics be banned?",
            "Should nuclear power be expanded?",
            "Should car-free zones be implemented in cities?"
        ]
    }

    # Topic selection
    category = st.selectbox("Select Debate Category", list(topics.keys()))
    topic = st.selectbox("Choose Your Topic", topics[category])

    # Debate preparation
    st.write("### Debate Preparation")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Pro Arguments**")
        st.text_area("Enter your pro arguments", key="pro")
        
    with col2:
        st.write("**Con Arguments**")
        st.text_area("Enter your con arguments", key="con")

    # Timer
    if st.button("Start Practice Timer"):
        st.write("⏱️ Practice Timer: 2:00")
        st.progress(0.5)

    # Feedback section
    st.write("### Peer Feedback")
    st.text_area("Give feedback to others", placeholder="Type your feedback here...")
