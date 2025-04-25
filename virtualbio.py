import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="VirtualBio - 3D Anatomy Viewer", layout="wide")

st.markdown("""
    <style>
        .main-title {
            font-size: 3em;
            font-weight: bold;
            color: #1CAAD9;
            text-align: center;
        }
        .sub-title {
            font-size: 1.5em;
            margin-top: 1em;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>🧬 VirtualBio - Interactive Anatomy Metaverse</div>", unsafe_allow_html=True)

organ = st.sidebar.selectbox("Choose an Organ to Explore", ["Heart", "Brain", "Kidney", "Liver", "Limbic System"])

educational_content = {
    "Heart": """
    **Anatomy of the Human Heart**
    
    - The heart has four chambers: right/left atria and right/left ventricles.
    - The right side pumps blood to the lungs, the left to the rest of the body.
    - Vena cava brings deoxygenated blood in; aorta takes oxygenated blood out.
    - Protected by the pericardium.
    """,
    "Brain": """
    **Anatomy of the Brain**
    
    - Divided into cerebrum, cerebellum, brainstem.
    - Controls cognition, emotions, movement, senses.
    - Cortex handles higher-order thinking.
    """,
    "Kidney": """
    **Anatomy of the Kidneys**
    
    - Filters waste from blood and forms urine.
    - Regulates electrolytes and fluid balance.
    - Nephrons are the functional units.
    """,
    "Liver": """
    **Anatomy of the Liver**
    
    - Processes nutrients, detoxifies chemicals, and produces bile.
    - Works with gallbladder and pancreas.
    - Highly vascular organ.
    """,
    "Limbic System": """
    **Limbic System Functions**
    
    - Controls emotions, memory, arousal.
    - Includes amygdala, hippocampus, hypothalamus.
    - Links smell and memory.
    """
}

model_embeds = {
    "Heart": """
        <iframe title="Heart Animated" frameborder="0" allowfullscreen mozallowfullscreen="true"
        webkitallowfullscreen="true" allow="autoplay; fullscreen; xr-spatial-tracking" xr-spatial-tracking
        execution-while-out-of-viewport execution-while-not-rendered web-share
        src="https://sketchfab.com/models/1582359649694207a2ad6bd0ebd0606a/embed"
        width="100%" height="480"></iframe>
    """,
    "Brain": """
        <iframe title="Brain" frameborder="0" allowfullscreen mozallowfullscreen="true"
        webkitallowfullscreen="true" allow="autoplay; fullscreen; xr-spatial-tracking" xr-spatial-tracking
        execution-while-out-of-viewport execution-while-not-rendered web-share
        src="https://sketchfab.com/models/3022543bb7a54b88b892ff4907e50929/embed"
        width="100%" height="480"></iframe>
    """,
    "Kidney": """
        <iframe title="Kidney" frameborder="0" allowfullscreen mozallowfullscreen="true"
        webkitallowfullscreen="true" allow="autoplay; fullscreen; xr-spatial-tracking" xr-spatial-tracking
        execution-while-out-of-viewport execution-while-not-rendered web-share
        src="https://sketchfab.com/models/686992c2a7fb456eaa8997b0366f4062/embed"
        width="100%" height="480"></iframe>
    """,
    "Liver": """
        <iframe title="Liver vasculature and bile ducts" frameborder="0" allowfullscreen mozallowfullscreen="true"
        webkitallowfullscreen="true" allow="autoplay; fullscreen; xr-spatial-tracking" xr-spatial-tracking
        execution-while-out-of-viewport execution-while-not-rendered web-share
        src="https://sketchfab.com/models/71f7790caa5743b8b64c7669f1c3a79c/embed"
        width="100%" height="480"></iframe>
    """,
    "Limbic System": """
        <iframe title="Limbic System Anatomy" frameborder="0" allowfullscreen mozallowfullscreen="true"
        webkitallowfullscreen="true" allow="autoplay; fullscreen; xr-spatial-tracking" xr-spatial-tracking
        execution-while-out-of-viewport execution-while-not-rendered web-share
        src="https://sketchfab.com/models/c9d4b17b2d584b898fd797863f4aceb8/embed"
        width="100%" height="480"></iframe>
    """
}

st.markdown("""
<div style='display: flex; justify-content: center;'>
""", unsafe_allow_html=True)
components.html(model_embeds[organ], height=500)
st.markdown("</div>", unsafe_allow_html=True)

# Show educational content
with st.expander(f"📘 Learn about the {organ}", expanded=True):
    st.markdown(educational_content[organ])

# Optional: Add quiz (basic example)
with st.expander("🧠 Quick Quiz", expanded=False):
    if organ == "Heart":
        q = st.radio("What does the left ventricle do?", [
            "Receives blood from lungs",
            "Pumps oxygenated blood to the body",
            "Supplies oxygen to heart walls"
        ])
        if q == "Pumps oxygenated blood to the body":
            st.success("Correct!")
        else:
            st.error("Try again!")