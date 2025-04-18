import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_sortables import sort_items
import google.generativeai as genai
import requests

# --- CONFIG ---
GENAI_API_KEY = "AIzaSyCV01--_lAYhn0ytZxmy1ZiaqNeLnX69UQ"
genai.configure(api_key=GENAI_API_KEY)

# --- SESSION INITIALIZATION ---
if "projects" not in st.session_state:
    st.session_state.projects = []

# --- GEMINI INTEGRATIONS ---
def query_gemini_flash(prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(f"Suggest 3 unique youth-led project ideas related to: {prompt}")
    return response.text.strip()

def generate_readme(description):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(f"Write a detailed README file with instructions on how to do this youth-led project:\n\n{description}")
    return response.text.strip()

# --- LOTTIE ANIMATION ---
def load_lottieurl(url: str):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

milestone_animation = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_w51pcehl.json")

# --- DYNAMIC SDG DATA ---
def get_dynamic_sdg_stats(topic):
    stats = {
        "Clean Energy": "⚡ Renewable energy use is projected to grow by 3.6% annually.",
        "Waste Management": "♻️ Over 2B tons of waste generated annually.",
        "Education Access": "📚 263M children globally lack school access.",
        "Digital Literacy": "💻 Only 54% of youth have basic digital skills."
    }
    return stats.get(topic, "📊 Real-time SDG data coming soon.")

# --- MAIN COMPONENT FUNCTION ---
def show_young_changemakers():
    st.title("🌍 YoungChangemakers: Project Lab")

    # --- Project Creation ---
    st.header("🚀 Create a Project")
    categories = {
        "Environmental": ["Clean Energy", "Waste Management", "Conservation"],
        "Social": ["Education Access", "Community Support", "Health Initiatives"],
        "Technology": ["Digital Literacy", "Tech for Good", "Innovation"]
    }

    category = st.selectbox("Select Category", list(categories.keys()))
    subcategory = st.selectbox("Select Focus Area", categories[category])

    if subcategory:
        suggestion = query_gemini_flash(subcategory)
        st.info(f"💡 Gemini Suggestions:\n\n{suggestion}")

    st.write(f"🌍 **SDG Insight:** {get_dynamic_sdg_stats(subcategory)}")

    project_name = st.text_input("Project Name")
    project_desc = st.text_area("Project Description")
    team_size = st.slider("Team Size", 1, 5, 2)

    if project_name and project_desc:
        st.subheader("📅 Planning")
        cols = st.columns(3)

        with cols[0]:
            goals = [st.text_input(f"Goal {i+1}") for i in range(3)]

        with cols[1]:
            weeks = st.number_input("Project Duration (weeks)", 1, 12, 4)

        with cols[2]:
            mentorship = st.checkbox("Mentorship")
            funding = st.checkbox("Funding")
            materials = st.checkbox("Materials")

        st.subheader("🧩 Task Planner")
        with st.expander("🎮 Plan your workflow"):
            col1, col2, col3 = st.columns(3)
            with col1:
                planning = sort_items("plan", ["Define goals", "Research issue"])
            with col2:
                in_progress = sort_items("progress", [])
            with col3:
                completed = sort_items("done", [])

        if st.button("✅ Submit Project"):
            st.session_state.projects.append({
                "name": project_name,
                "desc": project_desc,
                "category": category,
                "subcategory": subcategory,
                "team_size": team_size,
                "goals": goals,
                "weeks": weeks,
                "resources": {
                    "mentorship": mentorship,
                    "funding": funding,
                    "materials": materials
                },
                "tasks": {
                    "planning": planning,
                    "in_progress": in_progress,
                    "completed": completed
                }
            })
            st.success("🎉 Project submitted!")
            if milestone_animation:
                st_lottie(milestone_animation, height=250)
            st.balloons()

    # --- Submitted Projects ---
    st.header("📁 Submitted Projects")
    if not st.session_state.projects:
        st.info("No projects submitted yet.")
    else:
        for idx, project in enumerate(st.session_state.projects):
            with st.expander(f"📌 {project['name']}"):
                st.markdown(f"**Description:** {project['desc']}")
                st.markdown(f"**Category:** {project['category']} → {project['subcategory']}")
                st.markdown(f"**Team Size:** {project['team_size']}")
                st.markdown("**Goals:**")
                st.markdown("\n".join([f"- {g}" for g in project['goals'] if g.strip()]))
                st.markdown(f"**Duration:** {project['weeks']} weeks")
                st.markdown("**Resources Needed:**")
                for r, v in project['resources'].items():
                    if v:
                        st.markdown(f"- {r.capitalize()}")

                if st.button(f"📝 Generate README for {project['name']}", key=f"readme-{idx}"):
                    with st.spinner("Generating README..."):
                        readme = generate_readme(project['desc'])
                        st.code(readme, language="markdown")

    # --- Edit Projects ---
    st.header("✏️ Edit Projects")
    if not st.session_state.projects:
        st.info("No projects to edit.")
    else:
        for idx, project in enumerate(st.session_state.projects):
            with st.expander(f"✍️ Edit: {project['name']}"):
                new_name = st.text_input("Project Name", value=project["name"], key=f"name-{idx}")
                new_desc = st.text_area("Project Description", value=project["desc"], key=f"desc-{idx}")
                new_goals = [st.text_input(f"Goal {i+1}", value=project["goals"][i], key=f"goal-{idx}-{i}") for i in range(3)]
                new_weeks = st.number_input("Weeks", value=project["weeks"], key=f"weeks-{idx}")

                if st.button("💾 Save Changes", key=f"save-{idx}"):
                    project["name"] = new_name
                    project["desc"] = new_desc
                    project["goals"] = new_goals
                    project["weeks"] = new_weeks
                    st.success("✅ Changes saved.")