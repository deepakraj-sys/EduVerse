import streamlit as st
from datetime import datetime
import random
import time

def countdown_timer(total_seconds):
    placeholder = st.empty()
    for remaining in range(total_seconds, 0, -1):
        mins, secs = divmod(remaining, 60)
        timer_display = f"{mins:02d}:{secs:02d}"
        placeholder.markdown(f"## ⏳ Time Remaining: {timer_display}")
        time.sleep(1)
    placeholder.markdown("## ✅ Time's up!")
    st.balloons()

class AIContentGenerator:
    def get_learning_resources(self, subject, activity):
        descriptions = {
            "Math": {
                "Make Math Dinner": "Explore math concepts through cooking activities.",
                "Shopping Budget Challenge": "Learn budgeting and arithmetic through shopping scenarios.",
                "Geometric Garden": "Understand geometry by designing a garden."
            },
            "Grammar": {
                "Grammar Hunt at the Park": "Identify parts of speech in a park setting.",
                "Story Time Adventure": "Enhance storytelling and grammar skills.",
                "Word Detective": "Investigate and learn new words."
            },
            "Science": {
                "Science in the Kitchen": "Discover scientific principles through cooking.",
                "Backyard Biology": "Explore biology in your backyard.",
                "Weather Watch": "Learn about weather patterns and observation."
            }
        }

        sample_videos = {
            "Math": {
                "Make Math Dinner": [
                    {"url": "https://www.youtube.com/watch?v=yD1i3RRV2zg"}
                ],
                "Shopping Budget Challenge": [
                    {"url": "https://www.youtube.com/watch?v=Wvfrt9Os1f0"}
                ],
                "Geometric Garden": [
                    {"url": "https://www.youtube.com/watch?v=Ux_kLd7qAcY"}
                ]
            },
            "Grammar": {
                "Grammar Hunt at the Park": [
                    {"url": "https://www.youtube.com/watch?v=_LF0nWlnTgI"}
                ],
                "Story Time Adventure": [
                    {"url": "https://www.youtube.com/@Story_time_adventure"}
                ],
                "Word Detective": [
                    {"url": "https://www.youtube.com/watch?v=8HNndxNx9v8"}
                ]
            },
            "Science": {
                "Science in the Kitchen": [
                    {"url": "https://www.youtube.com/playlist?list=PLw2cuKNQvZ2c3y2d2hcS5mZ611VvgrAg6"}
                ],
                "Backyard Biology": [
                    {"url": "https://www.youtube.com/watch?v=2UtRFamOFTU"}
                ],
                "Weather Watch": [
                    {"url": "https://www.youtube.com/watch?v=Uo8lbeVVb4M"}
                ]
            }
        }

        return {
            "description": descriptions.get(subject, {}).get(activity, "Enjoy fun learning resources!"),
            "videos": sample_videos.get(subject, {}).get(activity, [])
        }

def run_parent_pal():
    st.title("ParentPal - Bridge Between Home and School")

    themes = {
        "Math": ["Make Math Dinner", "Shopping Budget Challenge", "Geometric Garden"],
        "Grammar": ["Grammar Hunt at the Park", "Story Time Adventure", "Word Detective"],
        "Science": ["Science in the Kitchen", "Backyard Biology", "Weather Watch"]
    }

    subject = st.selectbox("Select Subject", list(themes.keys()))
    activity = st.selectbox("Choose Activity", themes[subject])
    st.subheader(f"Today's Activity: {activity}")

    ai = AIContentGenerator()
    content = ai.get_learning_resources(subject, activity)

    if content:
        st.write("### Educational Resources")
        st.write(content.get("description", ""))
        for video in content.get("videos", []):
            st.video(video["url"])

    st.markdown("### Activity Instructions")
    instructions = generate_activity_instructions(subject, activity)
    st.write(instructions)

    with st.expander("Activity Materials"):
        materials = get_activity_materials(activity)
        for item in materials:
            st.checkbox(item)

    if st.button("Start Activity Timer"):
        countdown_timer(20 * 60)  # 20 minutes

    with st.form("reflection_form"):
        st.write("Track Your Progress")
        completion = st.slider("Activity Completion (%)", 0, 100, 50)
        enjoyment = st.slider("How fun was it? (1-5)", 1, 5, 3)
        learning = st.slider("How much did you learn? (1-5)", 1, 5, 3)
        reflection = st.text_area("Share your experience:")
        photo = st.file_uploader("Upload activity photos")
        submit = st.form_submit_button("Save Progress")

        if submit:
            st.success("Progress saved successfully!")
            if photo:
                st.image(photo, caption="Activity Photo")

            if completion >= 90:
                st.balloons()
                st.success("🏆 Achievement Unlocked: Super Learner!")

def generate_activity_instructions(subject, activity):
    instructions = {
        "Math": {
            "Make Math Dinner": "1. Count ingredients\n2. Measure portions\n3. Calculate cooking time\n4. Practice fractions with recipes\n5. Calculate total servings",
            "Shopping Budget Challenge": "1. Set a budget\n2. Compare prices\n3. Calculate total\n4. Find best deals\n5. Calculate savings",
            "Geometric Garden": "1. Identify shapes in nature\n2. Measure garden areas\n3. Design layout\n4. Calculate perimeter\n5. Plan plant spacing"
        },
        "Grammar": {
            "Grammar Hunt at the Park": "1. Find and list nouns\n2. Spot action verbs\n3. Create sentences\n4. Practice adjectives\n5. Make a story",
            "Story Time Adventure": "1. Choose characters\n2. Create plot outline\n3. Write story\n4. Add descriptions\n5. Read aloud",
            "Word Detective": "1. Find new words\n2. Look up meanings\n3. Use in sentences\n4. Find synonyms\n5. Create word games"
        },
        "Science": {
            "Science in the Kitchen": "1. Observe changes\n2. Record results\n3. Draw conclusions\n4. Test hypotheses\n5. Document findings",
            "Backyard Biology": "1. Identify plants\n2. Observe insects\n3. Record findings\n4. Draw specimens\n5. Create nature journal",
            "Weather Watch": "1. Check temperature\n2. Record conditions\n3. Track patterns\n4. Make predictions\n5. Create weather log"
        }
    }
    return instructions.get(subject, {}).get(activity, "No instructions available.")

def get_activity_materials(activity):
    materials_dict = {
        "Make Math Dinner": ["Measuring cups", "Calculator", "Recipe book", "Paper and pencil", "Timer"],
        "Shopping Budget Challenge": ["Calculator", "Shopping list", "Price comparison sheet", "Budget worksheet"],
        "Geometric Garden": ["Measuring tape", "Graph paper", "Ruler", "Garden planning sheet"],
        "Grammar Hunt at the Park": ["Notebook", "Pencil", "Word checklist", "Camera (optional)"],
        "Story Time Adventure": ["Story template", "Character cards", "Setting cards", "Plot outline"],
        "Word Detective": ["Dictionary", "Thesaurus", "Word journal", "Flashcards"],
        "Science in the Kitchen": ["Safety goggles", "Measuring tools", "Observation sheet", "Timer"],
        "Backyard Biology": ["Magnifying glass", "Collection jars", "Field guide", "Nature journal"],
        "Weather Watch": ["Thermometer", "Weather log", "Cloud chart", "Wind gauge"]
    }
    return materials_dict.get(activity, [])
