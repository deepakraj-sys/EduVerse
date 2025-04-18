"""BodyVerse Blueprint - Human-System Mapping Game for Biomedical Engineering"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
import json
import time
import random
from typing import List, Dict, Any, Optional

def run_bodyverse_header():
    """Display the header for BodyVerse Blueprint module."""
    st.markdown(
        """
        <div style="background-color:#3F51B5; padding:10px; border-radius:10px; margin-bottom:10px">
            <h1 style="color:white; text-align:center">
                <span style="font-size:1.5em">🧬</span> BodyVerse Blueprint <span style="font-size:1.5em">🧬</span>
            </h1>
            <h3 style="color:#E8EAF6; text-align:center">Human-System Mapping Game for Biomedical Engineering</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

def run_bodyverse_blueprint():
    """Main entry point for the BodyVerse Blueprint application."""
    run_bodyverse_header()

    # Sidebar with navigation
    st.sidebar.title("BodyVerse Navigation")

    # Navigation
    page = st.sidebar.radio(
        "Navigate to:",
        ["System Explorer", "Implant Explorer", "Disease Explorer", "Treatment Explorer", "Simulation"]
    )

    # Different pages
    if page == "System Explorer":
        display_system_explorer()
    elif page == "Implant Explorer":
        display_implant_explorer()
    elif page == "Disease Explorer":
        display_disease_explorer()
    elif page == "Treatment Explorer":
        display_treatment_explorer()
    elif page == "Simulation":
        display_simulation()

def display_system_explorer():
    """Display the system explorer section."""
    st.subheader("🔍 Human System Explorer")

    # Get sample systems
    systems = get_sample_systems()

    # System selection
    system_names = [system.name for system in systems]
    selected_system_name = st.selectbox("Select a system to explore:", system_names)

    # Find selected system
    selected_system = next((s for s in systems if s.name == selected_system_name), None)

    if selected_system:
        # Display system information
        st.markdown(f"## {selected_system.name}")
        st.markdown(selected_system.description)

        # Display components in an interactive 3D model
        display_3d_system_model(selected_system)

        # Educational content integration
        display_educational_content(selected_system)

        # Interactive quiz section
        display_system_quiz(selected_system)

def display_3d_system_model(system):
    """Display interactive 3D model of system components with animations."""
    st.subheader("Interactive 3D Model")

    # Generate mesh grid for surface
    x = np.linspace(-2, 2, 100)
    y = np.linspace(-2, 2, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(np.sqrt(X**2 + Y**2))

    # Create animated 3D visualization
    fig = go.Figure()

    # Add surface plot for main system
    fig.add_trace(go.Surface(
        x=X, y=Y, z=Z,
        colorscale='Viridis',
        showscale=False,
        opacity=0.8
    ))

    # Add component markers
    for i, comp in enumerate(system.components):
        fig.add_trace(go.Scatter3d(
            x=[np.cos(i * 2 * np.pi / len(system.components))],
            y=[np.sin(i * 2 * np.pi / len(system.components))],
            z=[1],
            mode='markers+text',
            text=[comp['name']],
            textposition='top center',
            marker=dict(
                size=15,
                color=['red', 'blue', 'green'][i % 3],
                symbol='circle'
            ),
            hoverinfo='text'
        ))

    # Add animation frames
    frames = []
    for t in np.linspace(0, 2*np.pi, 30):
        Z_animated = np.sin(np.sqrt(X**2 + Y**2) + t)
        frame = go.Frame(
            data=[
                go.Surface(x=X, y=Y, z=Z_animated, colorscale='Viridis', showscale=False, opacity=0.8)
            ] + [
                go.Scatter3d(
                    x=[np.cos(i * 2 * np.pi / len(system.components) + t)],
                    y=[np.sin(i * 2 * np.pi / len(system.components) + t)],
                    z=[np.sin(t) + 1],
                    mode='markers+text',
                    text=[comp['name']],
                    textposition='top center',
                    marker=dict(
                        size=15,
                        color=['red', 'blue', 'green'][i % 3],
                        symbol='circle'
                    )
                ) for i, comp in enumerate(system.components)
            ]
        )
        frames.append(frame)

    fig.frames = frames

    # Configure animation
    fig.update_layout(
        title=f"{system.name} Components",
        width=800,
        height=600,
        scene=dict(
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5)
            ),
            xaxis_title="X",
            yaxis_title="Y",
            zaxis_title="Z"
        ),
        updatemenus=[{
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": 100, "redraw": True}}],
                    "label": "Play",
                    "method": "animate"
                },
                {
                    "args": [[None], {"frame": {"duration": 0, "redraw": True}}],
                    "label": "Pause",
                    "method": "animate"
                }
            ],
            "type": "buttons"
        }]
    )

    st.plotly_chart(fig, use_container_width=True)

    # Add interactive controls
    st.sidebar.subheader("View Controls")
    rotation = st.sidebar.slider("Rotation", 0, 360, 180)
    zoom = st.sidebar.slider("Zoom", 0.5, 2.0, 1.0)

    fig.update_layout(
        scene_camera=dict(
            eye=dict(
                x=zoom * np.cos(np.radians(rotation)),
                y=zoom * np.sin(np.radians(rotation)),
                z=zoom
            )
        )
    )

    st.plotly_chart(fig, use_container_width=True)

def display_educational_content(system):
    """Display educational content from OpenStax."""
    st.subheader("Learn More")

    # Fetch content from OpenStax
    content = fetch_educational_content(system.id)

    if content:
        st.markdown(f"### {content['title']}")
        st.write(content['description'])

        # Display videos
        if content.get('videos'):
            st.markdown("#### Video Lessons")
            for video in content['videos']:
                st.markdown(f"📹 [{video['title']}]({video['url']})")
                st.markdown("---")

        # Display articles
        if content.get('articles'):
            st.markdown("#### Reading Materials")
            for article in content['articles']:
                st.markdown(f"📚 [{article['title']}]({article['url']})")
                st.markdown("---")

        # Display interactive content
        if content.get('interactive'):
            st.markdown("#### Interactive Learning")
            for item in content['interactive']:
                st.markdown(f"🔄 [{item['title']}]({item['url']})")
                st.markdown("---")

def display_system_quiz(system):
    """Display interactive quiz for the selected system."""
    st.subheader("Test Your Knowledge")

    # Get quiz from API
    quiz = fetch_system_quiz(system.id)

    if quiz:
        with st.form(key=f"quiz_{system.id}"):
            score = 0
            total_questions = len(quiz['questions'])

            for i, question in enumerate(quiz['questions']):
                st.write(f"**Question {i+1}:** {question['question']}")
                answer = st.radio("Select your answer:", question['options'], key=f"q_{i}")

                if st.form_submit_button(f"Check Answer {i+1}"):
                    if answer == question['answer']:
                        st.success("Correct!")
                        score += 1
                    else:
                        st.error(f"Incorrect. The right answer is: {question['answer']}")

            st.write(f"Score: {score}/{total_questions}")

def fetch_educational_content(topic: str) -> Dict[str, Any]:
    """
    Fetch educational content from OpenStax.
    For demonstration, using sample data instead of actual API call.
    """
    # OpenStax content mapping
    topics = {
        "circulatory": {
            "title": "The Circulatory System",
            "description": "The circulatory system consisting of the heart, blood vessels, and blood",
            "videos": [
                {
                    "title": "Heart Anatomy and Physiology",
                    "url": "https://openstax.org/details/video/heart-anatomy-physiology"
                }
            ],
            "articles": [
                {
                    "title": "Blood Vessel Structure and Function",
                    "url": "https://openstax.org/books/anatomy-and-physiology-2e/pages/18-1-an-overview-of-blood-vessel-structure-and-function"
                },
                {
                    "title": "Heart Anatomy",
                    "url": "https://openstax.org/books/anatomy-and-physiology-2e/pages/18-2-heart-anatomy"
                }
            ],
            "interactive": [
                {
                    "title": "Blood Flow Through the Heart",
                    "url": "https://openstax.org/books/anatomy-and-physiology-2e/pages/18-3-cardiac-cycle"
                }
            ]
        },
        "nervous": {
            "title": "The Nervous System",
            "description": "The nervous system and its components including neurons and synapses",
            "videos": [
                {
                    "title": "Neural Communication",
                    "url": "https://openstax.org/details/video/neural-communication"
                }
            ],
            "articles": [
                {
                    "title": "Basic Structure of the Nervous System",
                    "url": "https://openstax.org/books/anatomy-and-physiology-2e/pages/12-1-basic-structure-and-function-of-the-nervous-system"
                }
            ],
            "interactive": [
                {
                    "title": "Action Potential Generation",
                    "url": "https://openstax.org/books/anatomy-and-physiology-2e/pages/12-4-action-potential-generation"
                }
            ]
        }
    }
    
    return topics.get(topic, {
        "title": "General Anatomy",
        "description": "Basic anatomical concepts and terminology",
        "videos": [],
        "articles": [
            {
                "title": "Introduction to Anatomy",
                "url": "https://openstax.org/books/anatomy-and-physiology-2e/pages/1-introduction"
            }
        ],
        "interactive": []
    })

def fetch_system_quiz(system_id: str) -> Dict[str, Any]:
    """Fetch quiz questions for the system."""
    # Mock quiz data
    return {
        "questions": [
            {
                "question": "What is the main function of the circulatory system?",
                "options": [
                    "Transport nutrients and oxygen",
                    "Digest food",
                    "Filter blood",
                    "Produce hormones"
                ],
                "answer": "Transport nutrients and oxygen"
            }
        ]
    }


def fetch_educational_content(topic: str) -> Dict[str, Any]:
    """
    Fetch educational content from OpenStax.
    For demonstration, using sample data instead of actual API call.
    """
    # In a production app, we would implement the actual OpenStax API call
    topics = {
        "circulatory": {
            "title": "The Circulatory System",
            "description": "The circulatory system is a network of organs and vessels that transport blood throughout the body.",
            "videos": [
                {"title": "Introduction to the circulatory system", "duration": "8:20", "url": "https://openstax.org/details/books/anatomy-and-physiology/pages/18-1-overview-of-the-circulatory-system"},
                {"title": "The heart", "duration": "10:15", "url": "https://openstax.org/details/books/anatomy-and-physiology/pages/18-2-heart-anatomy"}
            ],
            "articles": [
                {"title": "Blood vessels", "url": "https://openstax.org/details/books/anatomy-and-physiology/pages/18-3-blood-vessel-structure-and-function"},
                {"title": "The lymphatic system", "url": "https://openstax.org/details/books/anatomy-and-physiology/pages/18-4-circulatory-pathways"}
            ]
        },
        "nervous": {
            "title": "The Nervous System",
            "description": "The nervous system is a complex network that controls bodily functions and activities.",
            "videos": [
                {"title": "Overview of neuron structure", "duration": "9:45", "url": "https://www.khanacademy.org/science/health-and-medicine/human-anatomy-and-physiology#nervous-system"},
                {"title": "The synapse", "duration": "12:30", "url": "https://www.khanacademy.org/science/health-and-medicine/human-anatomy-and-physiology#nervous-system"}
            ],
            "articles": [
                {"title": "The brain", "url": "https://www.khanacademy.org/science/health-and-medicine/human-anatomy-and-physiology#nervous-system"},
                {"title": "Neurotransmitters", "url": "https://www.khanacademy.org/science/health-and-medicine/human-anatomy-and-physiology#nervous-system"}
            ]
        },
        "musculoskeletal": {
            "title": "The Musculoskeletal System",
            "description": "The musculoskeletal system provides support, stability, and movement to the body.",
            "videos": [
                {"title": "Bones and skeletal tissues", "duration": "11:20", "url": "https://www.khanacademy.org/science/health-and-medicine/human-anatomy-and-physiology#musculoskeletal-system"},
                {"title": "Muscle contraction", "duration": "9:55", "url": "https://www.khanacademy.org/science/health-and-medicine/human-anatomy-and-physiology#musculoskeletal-system"}
            ],
            "articles": [
                {"title": "Joints", "url": "https://www.khanacademy.org/science/health-and-medicine/human-anatomy-and-physiology#musculoskeletal-system"},
                {"title": "Skeletal muscle", "url": "https://www.khanacademy.org/science/health-and-medicine/human-anatomy-and-physiology#musculoskeletal-system"}
            ]
        }
    }
    
    if topic in topics:
        return topics[topic]
    else:
        return {
            "title": "Human Body Systems",
            "description": "Learn about the various systems in the human body.",
            "videos": [],
            "articles": []
        }

def fetch_quizlet_quizzes(topic: str) -> List[Dict[str, Any]]:
    """
    Fetch quizzes from Quizlet API.
    For demonstration, using sample data instead of actual API call.
    """
    # In a production app, we would implement the actual API call
    quizzes = {
        "circulatory": [
            {
                "title": "Circulatory System Basics",
                "description": "Test your knowledge of the basic components and functions of the circulatory system.",
                "questions": [
                    {
                        "question": "What is the main function of the heart?",
                        "options": ["Filter blood", "Pump blood", "Produce blood cells", "Store blood"],
                        "answer": "Pump blood"
                    },
                    {
                        "question": "Which blood vessels carry blood away from the heart?",
                        "options": ["Arteries", "Veins", "Capillaries", "Arterioles"],
                        "answer": "Arteries"
                    }
                ]
            }
        ],
        "nervous": [
            {
                "title": "Nervous System Fundamentals",
                "description": "Test your understanding of basic nervous system components and functions.",
                "questions": [
                    {
                        "question": "What is the basic functional unit of the nervous system?",
                        "options": ["Neuron", "Brain", "Synapse", "Axon"],
                        "answer": "Neuron"
                    },
                    {
                        "question": "Which part of the neuron receives information from other neurons?",
                        "options": ["Dendrites", "Axon", "Cell body", "Myelin sheath"],
                        "answer": "Dendrites"
                    }
                ]
            }
        ],
        "musculoskeletal": [
            {
                "title": "Bones and Muscles Quiz",
                "description": "Test your knowledge of the skeletal and muscular systems.",
                "questions": [
                    {
                        "question": "How many bones are in the adult human body?",
                        "options": ["206", "176", "226", "156"],
                        "answer": "206"
                    },
                    {
                        "question": "Which type of muscle tissue is under voluntary control?",
                        "options": ["Cardiac muscle", "Smooth muscle", "Skeletal muscle", "All of the above"],
                        "answer": "Skeletal muscle"
                    }
                ]
            }
        ]
    }
    
    if topic in quizzes:
        return quizzes[topic]
    else:
        return []

# Data Models

class HumanSystem:
    def __init__(self, id: str, name: str, description: str, components: List[Dict[str, Any]]):
        self.id = id
        self.name = name
        self.description = description
        self.components = components

class Implant:
    def __init__(self, id: str, name: str, description: str, compatibility: List[str], cost: float):
        self.id = id
        self.name = name
        self.description = description
        self.compatibility = compatibility
        self.cost = cost

class Disease:
    def __init__(self, id: str, name: str, description: str, affected_systems: List[str], severity: float):
        self.id = id
        self.name = name
        self.description = description
        self.affected_systems = affected_systems
        self.severity = severity

class Treatment:
    def __init__(self, id: str, name: str, description: str, target_disease: str, effectiveness: float):
        self.id = id
        self.name = name
        self.description = description
        self.target_disease = target_disease
        self.effectiveness = effectiveness

# Sample Data

def get_sample_systems() -> List[HumanSystem]:
    """Get sample human systems."""
    return [
        HumanSystem(
            id="circulatory",
            name="Circulatory System",
            description="The circulatory system is a complex network of blood vessels that transport blood, oxygen, and nutrients throughout the body.",
            components=[
                {"name": "Heart", "function": "Pumps blood throughout the body", "image_url": "https://example.com/heart.jpg"},
                {"name": "Arteries", "function": "Carry oxygenated blood away from the heart", "image_url": "https://example.com/arteries.jpg"},
                {"name": "Veins", "function": "Return deoxygenated blood to the heart", "image_url": "https://example.com/veins.jpg"},
                {"name": "Capillaries", "function": "Allow exchange of nutrients and waste", "image_url": "https://example.com/capillaries.jpg"}
            ]
        ),
        HumanSystem(
            id="nervous",
            name="Nervous System",
            description="The nervous system is a complex network that controls and coordinates the body's activities, including voluntary and involuntary functions.",
            components=[
                {"name": "Brain", "function": "Central control center", "image_url": "https://example.com/brain.jpg"},
                {"name": "Spinal Cord", "function": "Main pathway for nerve signals", "image_url": "https://example.com/spinal_cord.jpg"},
                {"name": "Neurons", "function": "Transmit electrical signals", "image_url": "https://example.com/neurons.jpg"},
                {"name": "Synapses", "function": "Connect neurons to transmit signals", "image_url": "https://example.com/synapses.jpg"}
            ]
        ),
        HumanSystem(
            id="musculoskeletal",
            name="Musculoskeletal System",
            description="The musculoskeletal system provides form, support, stability, and movement to the body through bones, muscles, and joints.",
            components=[
                {"name": "Bones", "function": "Provide structure and protection", "image_url": "https://example.com/bones.jpg"},
                {"name": "Muscles", "function": "Generate force and movement", "image_url": "https://example.com/muscles.jpg"},
                {"name": "Joints", "function": "Allow movement between bones", "image_url": "https://example.com/joints.jpg"},
                {"name": "Tendons", "function": "Connect muscles to bones", "image_url": "https://example.com/tendons.jpg"}
            ]
        )
    ]

def get_sample_implants() -> List[Implant]:
    """Get sample implants."""
    return [
        Implant(
            id="artificial-heart-valve",
            name="Artificial Heart Valve",
            description="Replaces a damaged heart valve to regulate blood flow through the heart chambers.",
            compatibility=["circulatory"],
            cost=25000.0
        ),
        Implant(
            id="pacemaker",
            name="Cardiac Pacemaker",
            description="Regulates the heartbeat through electrical impulses delivered to the heart muscles.",
            compatibility=["circulatory"],
            cost=30000.0
        ),
        Implant(
            id="deep-brain-stimulator",
            name="Deep Brain Stimulator",
            description="Delivers electrical stimulation to targeted areas in the brain to treat movement disorders.",
            compatibility=["nervous"],
            cost=40000.0
        ),
        Implant(
            id="spinal-cord-stimulator",
            name="Spinal Cord Stimulator",
            description="Delivers mild electrical impulses to the spinal cord to treat chronic pain.",
            compatibility=["nervous"],
            cost=35000.0
        ),
        Implant(
            id="knee-replacement",
            name="Total Knee Replacement",
            description="Replaces a damaged knee joint with an artificial joint to improve mobility and reduce pain.",
            compatibility=["musculoskeletal"],
            cost=28000.0
        ),
        Implant(
            id="hip-replacement",
            name="Total Hip Replacement",
            description="Replaces a damaged hip joint with an artificial joint to improve mobility and reduce pain.",
            compatibility=["musculoskeletal"],
            cost=32000.0
        )
    ]

def get_sample_diseases() -> List[Disease]:
    """Get sample diseases."""
    return [
        Disease(
            id="coronary-artery-disease",
            name="Coronary Artery Disease",
            description="Narrowing or blockage of the coronary arteries that supply blood to the heart muscle.",
            affected_systems=["circulatory"],
            severity=0.8
        ),
        Disease(
            id="arrhythmia",
            name="Cardiac Arrhythmia",
            description="Irregular heartbeat caused by abnormal electrical activity in the heart.",
            affected_systems=["circulatory"],
            severity=0.7
        ),
        Disease(
            id="parkinsons",
            name="Parkinson's Disease",
            description="Progressive nervous system disorder that affects movement and causes tremors.",
            affected_systems=["nervous"],
            severity=0.9
        ),
        Disease(
            id="epilepsy",
            name="Epilepsy",
            description="Neurological disorder characterized by recurrent seizures.",
            affected_systems=["nervous"],
            severity=0.8
        ),
        Disease(
            id="osteoarthritis",
            name="Osteoarthritis",
            description="Degenerative joint disease that causes pain and stiffness in the joints.",
            affected_systems=["musculoskeletal"],
            severity=0.6
        ),
        Disease(
            id="rheumatoid-arthritis",
            name="Rheumatoid Arthritis",
            description="Autoimmune disease that causes inflammation and pain in multiple joints.",
            affected_systems=["musculoskeletal"],
            severity=0.7
        )
    ]

def get_sample_treatments() -> List[Treatment]:
    """Get sample treatments."""
    return [
        Treatment(
            id="valve-replacement",
            name="Heart Valve Replacement",
            description="Surgical procedure to replace a damaged heart valve with an artificial valve.",
            target_disease="coronary-artery-disease",
            effectiveness=0.85
        ),
        Treatment(
            id="pacemaker-implantation",
            name="Pacemaker Implantation",
            description="Surgical procedure to implant a pacemaker to regulate heart rhythm.",
            target_disease="arrhythmia",
            effectiveness=0.9
        ),
        Treatment(
            id="deep-brain-stimulation",
            name="Deep Brain Stimulation",
            description="Surgical procedure to implant a device that delivers electrical stimulation to specific areas of the brain.",
            target_disease="parkinsons",
            effectiveness=0.8
        ),
        Treatment(
            id="vagus-nerve-stimulation",
            name="Vagus Nerve Stimulation",
            description="Implanted device that delivers electrical stimulation to the vagus nerve to prevent seizures.",
            target_disease="epilepsy",
            effectiveness=0.75
        ),
        Treatment(
            id="knee-replacement-surgery",
            name="Total Knee Replacement Surgery",
            description="Surgical procedure to replace a damaged knee joint with an artificial joint.",
            target_disease="osteoarthritis",
            effectiveness=0.9
        ),
        Treatment(
            id="biologic-therapy",
            name="Biologic Therapy",
            description="Medication that targets specific components of the immune system to reduce inflammation.",
            target_disease="rheumatoid-arthritis",
            effectiveness=0.8
        )
    ]

# UI Components

def display_implant_explorer():
    """Display the implant explorer section."""
    st.subheader("🔧 Implant Explorer")
    
    # Get sample implants
    implants = get_sample_implants()
    
    # System filter
    systems = get_sample_systems()
    system_options = ["All Systems"] + [system.name for system in systems]
    selected_system_option = st.selectbox("Filter by compatible system:", system_options)
    
    # Apply filter
    filtered_implants = implants
    if selected_system_option != "All Systems":
        # Find system ID
        selected_system = next((s for s in systems if s.name == selected_system_option), None)
        if selected_system:
            filtered_implants = [i for i in implants if selected_system.id in i.compatibility]
    
    # Display implants
    if filtered_implants:
        for implant in filtered_implants:
            with st.expander(implant.name):
                st.markdown(implant.description)
                
                # Compatible systems
                compatible_system_names = []
                for system_id in implant.compatibility:
                    system = next((s for s in systems if s.id == system_id), None)
                    if system:
                        compatible_system_names.append(system.name)
                
                st.markdown(f"**Compatible Systems:** {', '.join(compatible_system_names)}")
                st.markdown(f"**Cost:** ${implant.cost:,.2f}")
                
                # In a real app, we would display more details and maybe 3D models
                st.markdown("*3D model placeholder*")

def display_disease_explorer():
    """Display the disease explorer section."""
    st.subheader("🦠 Disease Explorer")
    
    # Get sample diseases
    diseases = get_sample_diseases()
    
    # System filter
    systems = get_sample_systems()
    system_options = ["All Systems"] + [system.name for system in systems]
    selected_system_option = st.selectbox("Filter by affected system:", system_options)
    
    # Apply filter
    filtered_diseases = diseases
    if selected_system_option != "All Systems":
        # Find system ID
        selected_system = next((s for s in systems if s.name == selected_system_option), None)
        if selected_system:
            filtered_diseases = [d for d in diseases if selected_system.id in d.affected_systems]
    
    # Display diseases
    if filtered_diseases:
        for disease in filtered_diseases:
            # Determine severity class
            severity_class = ""
            if disease.severity >= 0.8:
                severity_class = "high"
            elif disease.severity >= 0.6:
                severity_class = "medium"
            else:
                severity_class = "low"
            
            with st.expander(f"{disease.name} (Severity: {severity_class})"):
                st.markdown(disease.description)
                
                # Affected systems
                affected_system_names = []
                for system_id in disease.affected_systems:
                    system = next((s for s in systems if s.id == system_id), None)
                    if system:
                        affected_system_names.append(system.name)
                
                st.markdown(f"**Affected Systems:** {', '.join(affected_system_names)}")
                
                # Severity bar
                st.progress(disease.severity)
                st.markdown(f"**Severity:** {disease.severity * 100:.0f}%")

def display_treatment_explorer():
    """Display the treatment explorer section."""
    st.subheader("💉 Treatment Explorer")
    
    # Get sample treatments and diseases
    treatments = get_sample_treatments()
    diseases = get_sample_diseases()
    
    # Disease filter
    disease_options = ["All Diseases"] + [disease.name for disease in diseases]
    selected_disease_option = st.selectbox("Filter by target disease:", disease_options)
    
    # Apply filter
    filtered_treatments = treatments
    if selected_disease_option != "All Diseases":
        # Find disease ID
        selected_disease = next((d for d in diseases if d.name == selected_disease_option), None)
        if selected_disease:
            filtered_treatments = [t for t in treatments if t.target_disease == selected_disease.id]
    
    # Display treatments
    if filtered_treatments:
        for treatment in filtered_treatments:
            with st.expander(treatment.name):
                st.markdown(treatment.description)
                
                # Target disease
                target_disease = next((d for d in diseases if d.id == treatment.target_disease), None)
                if target_disease:
                    st.markdown(f"**Target Disease:** {target_disease.name}")
                
                # Effectiveness
                st.progress(treatment.effectiveness)
                st.markdown(f"**Effectiveness:** {treatment.effectiveness * 100:.0f}%")

def display_simulation():
    """Display the simulation section."""
    st.subheader("🧪 Disease & Treatment Simulator")
    
    st.write("""
    This simulator allows you to test the effectiveness of different treatments on various diseases.
    Select a system, disease, and treatment to see the results.
    """)
    
    # Get data
    systems = get_sample_systems()
    diseases = get_sample_diseases()
    treatments = get_sample_treatments()
    implants = get_sample_implants()
    
    # Step 1: Select system
    st.markdown("### Step 1: Select a Human System")
    system_names = [system.name for system in systems]
    selected_system_name = st.selectbox("Select a system:", system_names)
    selected_system = next((s for s in systems if s.name == selected_system_name), None)
    
    if not selected_system:
        st.error("Please select a valid system.")
        return
    
    # Step 2: Select disease
    st.markdown("### Step 2: Select a Disease")
    # Filter diseases by selected system
    system_diseases = [d for d in diseases if selected_system.id in d.affected_systems]
    
    if not system_diseases:
        st.warning(f"No diseases found for the {selected_system_name}.")
        return
    
    disease_names = [disease.name for disease in system_diseases]
    selected_disease_name = st.selectbox("Select a disease:", disease_names)
    selected_disease = next((d for d in system_diseases if d.name == selected_disease_name), None)
    
    if not selected_disease:
        st.error("Please select a valid disease.")
        return
    
    # Step 3: Select treatment
    st.markdown("### Step 3: Select a Treatment")
    # Filter treatments by selected disease
    disease_treatments = [t for t in treatments if t.target_disease == selected_disease.id]
    
    if not disease_treatments:
        st.warning(f"No treatments found for {selected_disease_name}.")
        return
    
    treatment_names = [treatment.name for treatment in disease_treatments]
    selected_treatment_name = st.selectbox("Select a treatment:", treatment_names)
    selected_treatment = next((t for t in disease_treatments if t.name == selected_treatment_name), None)
    
    if not selected_treatment:
        st.error("Please select a valid treatment.")
        return
    
    # Step 4: Select implants (if applicable)
    st.markdown("### Step 4: Select Implants (if applicable)")
    # Filter implants by selected system
    system_implants = [i for i in implants if selected_system.id in i.compatibility]
    
    if system_implants:
        implant_options = [implant.name for implant in system_implants]
        selected_implant_names = st.multiselect("Select implants:", implant_options)
        selected_implants = [i for i in system_implants if i.name in selected_implant_names]
    else:
        st.info(f"No implants available for the {selected_system_name}.")
        selected_implants = []
    
    # Run simulation
    st.markdown("### Step 5: Run Simulation")
    
    run_simulation = st.button("Run Simulation")
    
    if run_simulation:
        with st.spinner("Running simulation..."):
            # Add a slight delay to give a feeling of computation
            time.sleep(2)
            
            # In a real app, we would run a more complex simulation
            # For demo purposes, we'll use a simple calculation
            
            # Base effectiveness from treatment
            effectiveness = selected_treatment.effectiveness * 100
            
            # Implants can improve effectiveness slightly
            if selected_implants:
                effectiveness_boost = len(selected_implants) * 5  # 5% per implant
                effectiveness = min(100, effectiveness + effectiveness_boost)
            
            # Disease severity reduces effectiveness
            severity_penalty = selected_disease.severity * 20  # Up to 20% reduction
            effectiveness = max(0, effectiveness - severity_penalty)
            
            # Display results
            st.success("Simulation completed!")
            
            # Results visualization
            st.subheader("Simulation Results")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Treatment Effectiveness", f"{effectiveness:.1f}%")
                
                # Display visual effectiveness
                if effectiveness >= 80:
                    st.success("This treatment is highly effective for this disease.")
                elif effectiveness >= 60:
                    st.warning("This treatment is moderately effective for this disease.")
                else:
                    st.error("This treatment has limited effectiveness for this disease.")
            
            with col2:
                # Cost calculation
                treatment_cost = 50000  # Base cost
                implant_cost = sum(implant.cost for implant in selected_implants)
                total_cost = treatment_cost + implant_cost
                
                st.metric("Total Cost", f"${total_cost:,.2f}")
                
                # FDA constraints
                st.info("This treatment meets FDA guidelines and constraints.")
            
            # Time-series recovery visualization
            st.subheader("Patient Recovery Projection")
            
            # Generate time-series data
            months = list(range(12))
            recovery_rate = effectiveness / 100
            
            # Without treatment
            no_treatment = [min(100, selected_disease.severity * 100 * (1 + 0.1 * month)) for month in months]
            
            # With treatment
            with_treatment = [max(0, selected_disease.severity * 100 * (1 - recovery_rate * min(1, month / 3))) for month in months]
            
            # Create dataframe for plotting
            df = pd.DataFrame({
                'Month': months,
                'Without Treatment': no_treatment,
                'With Treatment': with_treatment
            })
            
            # Plot
            fig = px.line(df, x='Month', y=['Without Treatment', 'With Treatment'],
                         labels={'value': 'Disease Severity (%)', 'variable': 'Scenario'},
                         title='Disease Progression Over Time')
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Recommendations
            st.subheader("Recommendations")
            
            if effectiveness >= 80:
                st.markdown("""
                **Recommended Course of Action**
                
                This treatment plan shows excellent potential for managing the disease effectively.
                
                - Proceed with the proposed treatment
                - Schedule follow-up evaluations at 1, 3, and 6 months
                - Monitor for potential side effects
                """)
            elif effectiveness >= 60:
                st.markdown("""
                **Recommended Course of Action**
                
                This treatment plan shows moderate effectiveness and may need supplementation.
                
                - Consider additional therapeutic approaches
                -Schedule more frequent follow-up evaluations
                - Explore alternative treatments if symptoms persist
                """)
            else:
                st.markdown("""
                **Recommended Course of Action**
                
                This treatment plan shows limited effectiveness for this condition.
                
                - Consider alternative treatment approaches
                - Consult with specialists for more targeted interventions
                - Focus on symptom management while exploring other options
                """)

# Main Application Function

def run_bodyverse_header():
    """Display the header for BodyVerse Blueprint module."""
    st.markdown(
        """
        <div style="background-color:#3F51B5; padding:10px; border-radius:10px; margin-bottom:10px">
            <h1 style="color:white; text-align:center">
                <span style="font-size:1.5em">🧬</span> BodyVerse Blueprint <span style="font-size:1.5em">🧬</span>
            </h1>
            <h3 style="color:#E8EAF6; text-align:center">Human-System Mapping Game for Biomedical Engineering</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

def run_bodyverse_blueprint():
    """Main entry point for the BodyVerse Blueprint application."""
    run_bodyverse_header()

    # Sidebar with navigation
    st.sidebar.title("BodyVerse Navigation")

    # Navigation
    page = st.sidebar.radio(
        "Navigate to:",
        ["System Explorer", "Implant Explorer", "Disease Explorer", "Treatment Explorer", "Simulation"]
    )

    # Different pages
    if page == "System Explorer":
        display_system_explorer()
    elif page == "Implant Explorer":
        display_implant_explorer()
    elif page == "Disease Explorer":
        display_disease_explorer()
    elif page == "Treatment Explorer":
        display_treatment_explorer()
    elif page == "Simulation":
        display_simulation()

if __name__ == "__main__":
    run_bodyverse_blueprint()