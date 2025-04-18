import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import requests
from datetime import datetime
from streamlit_drawable_canvas import st_canvas
from fpdf import FPDF
import base64
from streamlit_lottie import st_lottie
from streamlit_folium import st_folium
import folium

def load_lottie_json(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
        else:
            st.error(f"Error fetching Lottie animation: {r.status_code}")
            return None
    except Exception as e:
        st.error(f"Exception occurred: {str(e)}")
        return None

def show_animated_avatar(role):
    avatars = {
        "Water Wizard": "https://assets9.lottiefiles.com/packages/lf20_tutvdkg0.json",
        "Traffic Tactician": "https://assets4.lottiefiles.com/packages/lf20_L7Yrbx.json",
        "Green Guardian": "https://assets10.lottiefiles.com/packages/lf20_sFq3Xj.json"
    }
    lottie_json = load_lottie_json(avatars.get(role))
    if lottie_json is None:
        st.error(f"Failed to load animation for {role}. Please check the Lottie URL.")
    else:
        st_lottie(lottie_json, height=180, key=role)

def get_sdg_insights(policy_card):
    sdg_map = {
        "Eco-Friendly": {
            "SDG": "SDG 13 - Climate Action",
            "Description": "Take urgent action to combat climate change and its impacts.",
            "Lottie": "https://assets10.lottiefiles.com/packages/lf20_j1adxtyb.json"
        },
        "Fast Mobility": {
            "SDG": "SDG 11 - Sustainable Cities and Communities",
            "Description": "Make cities inclusive, safe, resilient and sustainable.",
            "Lottie": "https://assets6.lottiefiles.com/private_files/lf30_gqzddj3c.json"
        },
        "Resilient Infrastructure": {
            "SDG": "SDG 9 - Industry, Innovation and Infrastructure",
            "Description": "Build resilient infrastructure, promote sustainable industrialization.",
            "Lottie": "https://assets5.lottiefiles.com/packages/lf20_d3d7fctu.json"
        }
    }
    return sdg_map.get(policy_card, {})

def simulate_city_metrics(water_infra, green_space, traffic_opt, time_periods=24):
    base_traffic = np.random.normal(1000, 200, time_periods)
    base_flooding = np.random.normal(10, 5, time_periods)
    base_pollution = np.random.normal(50, 10, time_periods)

    traffic_flow = base_traffic * (1 - 0.2 * traffic_opt)
    flood_risk = base_flooding * (1 - 0.3 * water_infra)
    air_quality = base_pollution * (1 - 0.25 * green_space)

    return traffic_flow, flood_risk, air_quality

def generate_pdf_report(metrics):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="CivilVerse Simulation Report", ln=True, align='C')
    pdf.ln(10)
    for key, value in metrics.items():
        pdf.cell(200, 10, txt=f"{key}: {value:.1f}%", ln=True)
    pdf.cell(200, 10, txt="Suggested SDG Alignment: SDG 11 - Sustainable Cities", ln=True)

    pdf_file = "city_report.pdf"
    pdf.output(pdf_file)
    return pdf_file

def get_live_aqi(city="Chennai"):
    try:
        url = f"https://api.openaq.org/v2/latest?city={city}"
        response = requests.get(url)
        data = response.json()

        results = data.get("results", [])
        if not results:
            st.warning(f"No AQI data found for {city}. Try another city.")
            return None

        for item in results:
            for measure in item.get("measurements", []):
                if measure["parameter"] in ["pm25", "pm10"]:
                    return measure["value"]
        st.warning(f"No PM2.5 or PM10 data available for {city} right now.")
        return None
    except Exception as e:
        st.error(f"API Error: {e}")
        return None

def show_live_map():
    st.subheader("🗺️ Real-Time City Map")
    m = folium.Map(location=[13.0827, 80.2707], zoom_start=12)  # Chennai coordinates
    st_folium(m, width=700, height=500)

def infrastructure_map():
    st.subheader("🛠️ Infrastructure Canvas")
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=2,
        background_color="#f0f0f0",
        update_streamlit=True,
        height=300,
        drawing_mode="freedraw",
        key="canvas",
    )
    return canvas_result

def scenario_and_budget():
    st.subheader("Scenario and Budget")
    scenario = st.selectbox("Choose Scenario", ["Coastal City", "Desert Town", "Mountain Valley"])
    budget = st.slider("City Planning Budget (in ₹ Lakhs)", 100, 10000, 2500, step=100)
    policy = st.selectbox("Policy Card", ["Eco-Friendly", "Fast Mobility", "Resilient Infrastructure"])
    st.progress(budget / 10000)
    return scenario, budget, policy

def run_civilverse():
    st.title("🌆 CivilVerse: The City Builder Classroom")
    st.write("Collaborative city planning and infrastructure simulation")

    role = st.selectbox("Select Your Team Role", ["Water Wizard", "Traffic Tactician", "Green Guardian"])
    show_animated_avatar(role)

    scenario, budget, policy = scenario_and_budget()

    city_choice = st.text_input("Enter a city name for AQI data", "Chennai")  # Default city is Chennai

    sdg_data = get_sdg_insights(policy)
    if sdg_data:
        st.subheader("🌍 SDG Alignment Insight")
        st.markdown(f"**{sdg_data['SDG']}**")
        st.info(sdg_data["Description"])
        st_lottie(load_lottie_json(sdg_data["Lottie"]), height=180, key="sdg_lottie")

    st.subheader("Infrastructure Planning")
    col1, col2, col3 = st.columns(3)
    with col1:
        water_infra = st.slider("Water Infrastructure", 0.0, 1.0, 0.5)
    with col2:
        green_space = st.slider("Green Infrastructure", 0.0, 1.0, 0.5)
    with col3:
        traffic_opt = st.slider("Traffic Optimization", 0.0, 1.0, 0.5)

    infrastructure_map()
    show_live_map()

    if st.button("Run Simulation"):
        hours = list(range(24))
        traffic_flow, flood_risk, air_quality = simulate_city_metrics(water_infra, green_space, traffic_opt)

        st.plotly_chart(go.Figure([go.Scatter(x=hours, y=traffic_flow, name="Traffic Flow")])
                        .update_layout(title="24-Hour Traffic Flow Simulation"))
        st.plotly_chart(go.Figure([go.Scatter(x=hours, y=flood_risk, name="Flood Risk")])
                        .update_layout(title="Flood Risk Assessment"))
        st.plotly_chart(go.Figure([go.Scatter(x=hours, y=air_quality, name="Air Quality")])
                        .update_layout(title="Air Quality Index"))

        metrics = {
            "Traffic Efficiency": (1000 - np.mean(traffic_flow)) / 1000 * 100,
            "Flood Resilience": (20 - np.mean(flood_risk)) / 20 * 100,
            "Air Quality Score": (100 - np.mean(air_quality)) / 100 * 100
        }

        st.subheader("City Performance Metrics")
        cols = st.columns(3)
        for i, (metric, value) in enumerate(metrics.items()):
            with cols[i]:
                st.metric(metric, f"{value:.1f}%")

        report_file = generate_pdf_report(metrics)
        with open(report_file, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            href = f'<a href="data:application/pdf;base64,{b64}" download="city_report.pdf">📄 Download Report</a>'
            st.markdown(href, unsafe_allow_html=True)

    st.subheader("Team Collaboration")
    with st.form("team_notes"):
        notes = st.text_area("Add notes for your team")
        submitted = st.form_submit_button("Share Notes")
        if submitted and notes:
            st.success("Notes shared with team")

    st.subheader("Live Environmental Data")
    aqi = get_live_aqi(city_choice)
    if aqi:
        st.info(f"🌫️ Current PM2.5/PM10 AQI (from OpenAQ): {aqi}")
    else:
        st.warning("⚠️ Could not retrieve AQI data. Please check API availability.")

if __name__ == "__main__":
    run_civilverse()