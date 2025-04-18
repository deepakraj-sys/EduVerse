import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import pyvista as pv
import streamlit.components.v1 as components
import folium
from streamlit_folium import st_folium
from educational_api_connector import APIConnector
import time
import os

class StructuralCase:
    def __init__(self, name, year, description, factors, data, location, structure_type, history):
        self.name = name
        self.year = year
        self.description = description
        self.factors = factors
        self.data = data
        self.location = location
        self.structure_type = structure_type
        self.history = history

def get_sample_cases(): 
    cases = {
        "tacoma": StructuralCase(
            "Tacoma Narrows Bridge",
            1940,
            "The Tacoma Narrows Bridge collapsed due to aeroelastic flutter. The Tacoma Narrows Bridge, often nicknamed \"Galloping Gertie,\" became one of the most infamous examples of structural failure in engineering history when it dramatically collapsed on November 7, 1940, just four months after its opening. Located in the state of Washington, USA, this suspension bridge was designed to span the Tacoma Narrows strait of Puget Sound between the cities of Tacoma and the Kitsap Peninsula. It was the third-longest suspension bridge in the world at the time, following the Golden Gate and George Washington bridges, with a central span of 2,800 feet (853 meters). Despite its grand scale and importance, the bridge’s demise became a defining case study in the fields of aerodynamics, structural engineering, and resonance-induced vibration. ...",
            ["Wind-induced vibration", "Resonance", "Insufficient damping"],
            {
                "wind_speed": np.random.normal(35, 5, 50),
                "oscillation": np.random.normal(0, 1, 50) * np.sin(np.linspace(0, 10, 50))
            },
            location=(47.269, -122.551),
            structure_type="Bridge",
            history="The Tacoma Narrows Bridge opened in July 1940 and dramatically collapsed in November 1940 due to wind-induced oscillations. The structure's slender design and inadequate aerodynamic stability led to its destruction. The event emphasized the need for aerodynamic testing and simulations, influencing the future of suspension bridge designs globally."
        ),
        "morandi": StructuralCase(
            "Morandi Bridge",
            2018,
            "The Morandi Bridge collapsed due to structural degradation and severe weather. The Morandi Bridge, officially known as the Ponte Morandi, was a key motorway viaduct in Genoa, Italy, completed in 1967 and designed by Italian civil engineer Riccardo Morandi. It was a vital section of the A10 motorway, serving as a crucial link between the Italian Riviera and northern Italy, carrying thousands of vehicles daily. On August 14, 2018, a large section of the bridge tragically collapsed during a severe rainstorm, leading to the deaths of 43 people and injuring many more. The collapse shocked Italy and the global engineering community, raising urgent questions about infrastructure safety, aging bridges, and maintenance practices. The Morandi Bridge was known for its unique design that combined prestressed concrete with cable-stayed structures — a rare hybrid design at the time. ...",
            ["Concrete degradation", "Steel corrosion", "Maintenance issues"],
            {
                "strain": np.random.normal(100, 15, 50) + np.linspace(0, 50, 50),
                "corrosion": np.random.normal(0, 1, 50) * np.exp(np.linspace(0, 1, 50))
            },
            location=(44.414, 8.918),
            structure_type="Bridge",
            history="Constructed in the 1960s, the Morandi Bridge served as a vital artery in Genoa. Over decades, corrosion of the steel cables and concrete degradation worsened due to marine air and insufficient maintenance. Despite numerous inspections, the structure failed on August 14, 2018, during a storm, killing 43 people and prompting a complete reevaluation of Italian infrastructure policies."
        ),
        "lian_yun_gang": StructuralCase(
            "Lian Yungang Cooling Tower",
            2016,
            "Cooling tower collapse due to scaffold failure during construction.",
            ["Scaffolding instability", "Construction mismanagement", "High wind conditions"],
            {
                "wind_pressure": np.random.normal(60, 10, 50),
                "vibration": np.random.normal(0.5, 0.1, 50)
            },
            location=(34.658, 119.257),
            structure_type="Cooling Tower",
            history="The Lian Yungang cooling tower accident in Jiangsu Province, China, killed 74 construction workers in 2016. The primary cause was the collapse of a scaffold while concrete was being poured at the top level. Investigations revealed insufficient bracing and rushed schedules. The tragedy underscored the need for rigorous safety audits and worker protection laws, especially for temporary structures."
        ),
        "mecca": StructuralCase(
            "Mecca Crane Collapse",
            2015,
            "Crane collapsed at the Grand Mosque due to extreme wind during a thunderstorm. The Mecca Crane Collapse, one of the deadliest crane accidents in history, occurred on September 11, 2015, at the Masjid al-Haram (Grand Mosque) in Mecca, Saudi Arabia. The incident happened just days before the annual Hajj pilgrimage, one of the largest religious gatherings in the world. A massive crawler crane, operated by the Saudi Binladin Group, collapsed during a heavy storm...",
            ["Crane failure", "Severe weather", "Construction risks"],
            {
                "wind_speed": np.random.normal(80, 10, 50),
                "load": np.random.normal(200, 25, 50)
            },
            location=(21.4225, 39.8262),
            structure_type="Crane",
            history="The Mecca crane collapse in 2015 was caused by extreme weather and led to over 100 fatalities. It exposed vulnerabilities in safety planning and weather response for large-scale construction projects, particularly during high-traffic religious events."
        )
    }
    return cases

def display_3d_simulation(case):
    st.subheader("🌀 3D Interactive Simulation")
    st.caption("Explore structure response based on parameters like wind and load")
    wind_speed = st.slider("Wind Speed", 0, 100, 30)
    load = st.slider("Load", 0, 100, 50)

    plotter = pv.Plotter(off_screen=True, window_size=[600, 600])
    if case.structure_type == "Bridge":
        beam = pv.Box(bounds=(-2, 2, -0.2, 0.2, -0.1, 0.1))
    else:
        beam = pv.Cube(center=(0, 0, 0), x_length=2, y_length=2, z_length=10)

    beam.points[:, 2] += 0.01 * np.sin(beam.points[:, 0] * wind_speed / 10 + load / 10)
    plotter.add_mesh(beam, color="steelblue")
    plotter.set_background("white")
    plotter.show(screenshot="temp.png")
    st.image("temp.png")

def fix_simulator():
    st.subheader("🔧 Enhanced Fix Simulator")
    st.caption("Try structural reinforcements and design alternatives")

    damping = st.slider("Damping Coefficient", 0.0, 1.0, 0.3)
    material_quality = st.selectbox("Material Type", ["Standard Steel", "Reinforced Steel", "Carbon Fiber", "Smart Concrete"])
    sensors = st.checkbox("Add Structural Health Monitoring Sensors")
    emergency_protocol = st.checkbox("Simulate Emergency Protocols")

    risk_reduction = damping * 30
    if material_quality == "Reinforced Steel":
        risk_reduction += 30
    elif material_quality == "Carbon Fiber":
        risk_reduction += 50
    elif material_quality == "Smart Concrete":
        risk_reduction += 40

    if sensors:
        risk_reduction += 20
    if emergency_protocol:
        risk_reduction += 10

    st.metric("Projected Failure Risk Reduction", f"{min(int(risk_reduction), 100)}%")

def challenge_mode(case):
    st.subheader("🎯 Challenge Mode")
    with st.expander("🧠 Timed Challenge - Identify Key Failure Causes"):
        start_time = time.time()
        correct_factors = set(case.factors)
        user_answers = st.multiselect("Select Likely Failure Factors", [
            "Wind-induced vibration", "Resonance", "Insufficient damping",
            "Concrete degradation", "Steel corrosion", "Maintenance issues",
            "Seismic activity", "Design flaw", "Extreme weather",
            "Scaffolding instability", "Operational oversight"
        ])

        if st.button("Submit Challenge"):
            score = len(correct_factors.intersection(user_answers)) * 10
            time_taken = int(time.time() - start_time)
            st.success(f"✅ Score: {score} points")
            st.info(f"⏱️ Time taken: {time_taken} seconds")

def show_global_map(cases):
    st.subheader("📜 Global Structural Failures Map")
    m = folium.Map(location=[20, 0], zoom_start=2)
    type_filter = st.selectbox("Filter by Structure Type", ["All"] + list(set(c.structure_type for c in cases.values())))

    for case in cases.values():
        if type_filter != "All" and case.structure_type != type_filter:
            continue
        folium.Marker(
            location=case.location,
            tooltip=case.name,
            popup=f"{case.name} ({case.year}) - {case.structure_type}"
        ).add_to(m)

    st_data = st_folium(m, width=700, height=450)

def run_failure_vault():
    st.title("🏗️ Failure Vault - Forensic Engineering Explorer")
    st.write("Analyze historical structural failures, explore simulations, and learn real-time safety practices.")

    cases = get_sample_cases()
    selected_case_key = st.selectbox("Select Case Study", list(cases.keys()))
    case = cases[selected_case_key]

    st.subheader(f"{case.name} ({case.year})")
    st.write(case.description)
    st.info("**History:** " + case.history)

    st.subheader("Analysis Tools")
    tool = st.selectbox("Select Analysis Tool", [
        "Structural Data", "Factor Analysis", "Reconstruction",
        "3D Simulation", "Fix Simulator", "Challenge Mode", "Global Map"
    ])

    if tool == "Structural Data":
        fig = go.Figure()
        for key, values in case.data.items():
            fig.add_trace(go.Scatter(y=values, name=key))
        fig.update_layout(title="Structural Metrics Over Time")
        st.plotly_chart(fig)

    elif tool == "Factor Analysis":
        st.write("### Contributing Factors")
        for factor in case.factors:
            st.write(f"- {factor}")
        st.write("### Your Analysis")
        factor_importance = {factor: st.slider(f"Importance of {factor}", 0, 10, 5) for factor in case.factors}
        fig = px.bar(x=list(factor_importance.keys()), y=list(factor_importance.values()), title="Factor Importance Analysis")
        st.plotly_chart(fig)

    elif tool == "Reconstruction":
        st.write("### Reconstruction Planning")
        improvements = st.multiselect("Select proposed improvements", [
            "Enhanced structural monitoring", "Regular maintenance schedule",
            "Improved materials", "Better aerodynamic design", "Additional safety systems",
            "Emergency escape routes", "Seismic base isolation"])
        if improvements:
            st.success("Your proposed improvements have been recorded")
            improvement_score = len(improvements) * 15
            st.metric("Theoretical Safety Improvement", f"{min(improvement_score, 100)}%")

    elif tool == "3D Simulation":
        display_3d_simulation(case)

    elif tool == "Fix Simulator":
        fix_simulator()

    elif tool == "Challenge Mode":
        challenge_mode(case)

    elif tool == "Global Map":
        show_global_map(cases)

if __name__ == "__main__":
    run_failure_vault()