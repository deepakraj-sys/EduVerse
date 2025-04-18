import streamlit as st
from googleapiclient.discovery import build
import random
import json
import time

# YouTube API Setup
YOUTUBE_API_KEY = 'AIzaSyCu1PSjj7_JTYcrr3Df4rBJR3wT4M7-AHg'

def run_mathquest_land():
    st.title("🧙‍♂️ MathQuest Land")
    st.subheader("An Interactive Math Adventure")

    # Initialize API connector
    api = APIConnector()

    # Grade level selection
    grade = st.selectbox("Select Grade Level", ["K", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])

    # Game state management
    if 'player_stats' not in st.session_state:
        st.session_state.player_stats = {
            'level': 1,
            'points': 0,
            'quests_completed': 0,
            'characters_unlocked': ["Math Explorer"],
            'current_map': "Number Kingdom",
            'time_spent': 0,
            'last_activity': time.time()
        }

    # Display player stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Level", st.session_state.player_stats['level'])
    with col2:
        st.metric("Points", st.session_state.player_stats['points'])
    with col3:
        st.metric("Quests Completed", st.session_state.player_stats['quests_completed'])

    # Available quests
    st.subheader("📜 Available Quests")
    quests = {
        "Number Kingdom": "Master basic operations",
        "Fraction Forest": "Conquer fractions and decimals",
        "Geometry Gardens": "Explore shapes and measurements"
    }

    selected_quest = st.selectbox("Choose your quest", list(quests.keys()))
    st.write(f"### {selected_quest}")
    st.write(quests[selected_quest])

    # Interactive problem solving
    st.subheader("🎯 Challenge")
    problems = generate_math_problems(grade)
    for i, problem in enumerate(problems, 1):
        with st.form(f"math_problem_{i}"):
            st.write(f"Q{i}: {problem['question']}")
            if 'diagram' in problem:
                st.image(problem['diagram'], caption=f"Diagram for Q{i}", use_column_width=True)
            user_answer = st.number_input(f"Your answer for Q{i}:", step=0.1)
            submitted = st.form_submit_button(f"Submit Answer for Q{i}")

            if submitted:
                if abs(user_answer - problem['answer']) < 0.1:
                    st.success(f"Q{i} Correct! 🎉")
                    st.session_state.player_stats['points'] += 10
                    st.session_state.player_stats['quests_completed'] += 1

                    if st.session_state.player_stats['points'] >= st.session_state.player_stats['level'] * 100:
                        st.session_state.player_stats['level'] += 1
                        st.balloons()
                        st.success(f"Level Up! You're now level {st.session_state.player_stats['level']}!")
                else:
                    st.error(f"Q{i} Not quite right. Try again!")

    # Educational YouTube Videos
    st.subheader("📽️ Educational Videos")
    if grade in ["8", "9", "10"]:
        video_query = api.generate_video_query(selected_quest, grade)
        videos = api.get_youtube_videos(video_query)
        for video in videos:
            video_id = video['id']['videoId']
            st.video(f"https://www.youtube.com/watch?v={video_id}")
    else:
        st.info("Video content is currently focused on grades 8-10.")

    # Adaptive Learning Path
    st.subheader("🧠 Adaptive Learning Path")
    if st.session_state.player_stats['points'] < 50:
        st.write("You're still mastering the basics. Let's focus on foundational concepts.")
    elif st.session_state.player_stats['points'] < 100:
        st.write("Great progress! Time to tackle more challenging problems.")
    else:
        st.write("Excellent work! You're ready for advanced topics.")

    # Progress Dashboard for Parents
    if st.checkbox("Show Progress Dashboard"):
        st.subheader("📊 Progress Dashboard")
        progress_data = {
            'Concepts Mastered': st.session_state.player_stats['quests_completed'],
            'Total Practice Time': f"{st.session_state.player_stats['level'] * 10} minutes",
            'Accuracy Rate': f"{min(100, st.session_state.player_stats['points'] / 10)}%"
        }
        for metric, value in progress_data.items():
            st.metric(metric, value)

    # Time Management
    elapsed_time = time.time() - st.session_state.player_stats['last_activity']
    if elapsed_time > 3600:
        st.warning("You've been playing for over an hour. Consider taking a break.")

    # Update last activity time
    st.session_state.player_stats['last_activity'] = time.time()

class APIConnector:
    def __init__(self):
        self.youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

    def generate_video_query(self, quest, grade):
        base_query = f"cbse class {grade} math"
        if quest == "Number Kingdom":
            return f"{base_query} number system operations integers"
        elif quest == "Fraction Forest":
            return f"{base_query} fractions decimals rational numbers"
        elif quest == "Geometry Gardens":
            return f"{base_query} geometry triangles circles areas perimeters"
        return base_query

    def get_youtube_videos(self, query):
        try:
            request = self.youtube.search().list(
                part='snippet',
                q=query,
                type='video',
                maxResults=3,
                videoDuration='medium',
                relevanceLanguage='en'
            )
            response = request.execute()
            return response.get('items', [])
        except Exception as e:
            st.error(f"YouTube API error: {e}")
            return []

def generate_math_problems(grade):
    problems = {
        "1": [
            {"question": "What is 5 + 3?", "answer": 8},
            {"question": "What is 7 + 2?", "answer": 9},
            {"question": "What is 6 + 4?", "answer": 10},
            {"question": "What is 8 - 3?", "answer": 5},
            {"question": "What is 9 - 4?", "answer": 5},
            {"question": "What is 10 - 6?", "answer": 4},
            {"question": "What is 2 + 5?", "answer": 7},
            {"question": "What is 3 + 6?", "answer": 9},
            {"question": "What is 4 + 7?", "answer": 11},
            {"question": "What is 5 + 6?", "answer": 11}
        ],
        "2": [
            # Number Kingdom
            {"question": "What is 12 + 15?", "answer": 27},
            {"question": "What is 30 - 14?", "answer": 16},
            {"question": "What is 6 × 4?", "answer": 24},
            {"question": "What is 45 ÷ 5?", "answer": 9},
            {"question": "What is 9 + 8 - 5?", "answer": 12},
            # Fraction Forest
            {"question": "What is 1/2 + 1/4?", "answer": 0.75},
            {"question": "What is 3/4 - 1/2?", "answer": 0.25},
            # Geometry Gardens
            {"question": "A rectangle has length 10 cm and width 5 cm. What is its area?", "answer": 50},
            {"question": "A square has a side length of 6 cm. What is its perimeter?", "answer": 24},
            {"question": "A triangle has sides of lengths 3 cm, 4 cm, and 5 cm. What is its perimeter?", "answer": 12}
        ],
        "3": [
            # Number Kingdom
            {"question": "What is 123 + 456?", "answer": 579},
            {"question": "What is 789 - 321?", "answer": 468},
            {"question": "What is 12 × 3?", "answer": 36},
            {"question": "What is 144 ÷ 12?", "answer": 12},
            {"question": "What is (8 + 6) × 2?", "answer": 28},
            # Fraction Forest
            {"question": "What is 2/3 + 1/6?", "answer": 0.8333},
            {"question": "What is 5/8 - 1/4?", "answer": 0.375},
            # Geometry Gardens
            {"question": "A rectangle has length 15 cm and width 4 cm. What is its perimeter?", "answer": 38},
            {"question": "A triangle has base 10 cm and height 5 cm. What is its area?", "answer": 25},
            {"question": "A circle has a radius of 7 cm. What is its circumference? (Use π ≈ 3.14)", "answer": 43.96}
        ],
        "4": [
            # Number Kingdom
            {"question": "What is 234 + 567?", "answer": 801},
            {"question": "What is 1000 - 456?", "answer": 544},
            {"question": "What is 23 × 4?", "answer": 92},
            {"question": "What is 144 ÷ 12?", "answer": 12},
            {"question": "What is (15 + 5) × 2?", "answer": 40},
            # Fraction Forest
            {"question": "What is 3/4 + 2/5?", "answer": 1.15},
            {"question": "What is 7/8 - 3/8?", "answer": 0.5},
            # Geometry Gardens
            {"question": "A square has a side length of 9 cm. What is its area?", "answer": 81},
            {"question": "A rectangle has length 12 cm and width 7 cm. What is its perimeter?", "answer": 38},
            {"question": "A triangle has sides of lengths 6 cm, 8 cm, and 10 cm. What is its perimeter?", "answer": 24}
        ],
        "5": [
            # Number Kingdom
            {"question": "What is 345 + 678?", "answer": 1023},
            {"question": "What is 1000 - 789?", "answer": 211},
            {"question": "What is 34 × 3?", "answer": 102},
            {"question": "What is 225 ÷ 15?", "answer": 15},
            {"question": "What is (20 + 10) × 3?", "answer": 90},
            # Fraction Forest
            {"question": "What is 5/6 + 1/3?", "answer": 1.5},
            {"question": "What is 7/8 - 1/2?", "answer": 0.375},
            # Geometry Gardens
            {"question": "A rectangle has length 14 cm and width 5 cm. What is its area?", "answer": 70},
            {"question": "A triangle has base 12 cm and height 6 cm. What is its area?", "answer": 36},
            {"question": "A circle has a diameter of 10 cm. What is its circumference? (Use π ≈ 3.14)", "answer": 31.4}
        ],
        "6": [
            # Number Kingdom
            {"question": "What is 456 + 789?", "answer": 1245},
            {"question": "What is 1500 - 678?", "answer": 822},
            {"question": "What is 45 × 6?", "answer": 270},
            {"question": "What is 360 ÷ 12?", "answer": 30},
            {"question": "What is (25 + 15) × 2?", "answer": 80},
            # Fraction Forest
            {"question": "What is 3/4 + 2/3?", "answer": 1.4167},
            {"question": "What is 7/8 - 5/12?", "answer": 0.4583},
            # Geometry Gardens
            {"question": "A rectangle has length 16 cm and width 9 cm. What is its perimeter?", "answer": 50,},
            {"question": "A triangle has sides of lengths 7 cm, 24 cm, and 25 cm. What is its perimeter?", "answer": 56},
            {"question": "A circle has a radius of 14 cm. What is its area? (Use π ≈ 3.14)", "answer": 615.44}
        ],
        "7": [
            # Number Kingdom
            {"question": "Evaluate: 5 + 3 × (12 - 7) ÷ 5^2", "answer": 5 + 3 * (12 - 7) / 25},
            {"question": "Simplify: (28 ÷ 4) × 3 - 2 + 5^2", "answer": (28 / 4) * 3 - 2 + 25},
            {"question": "Find the value: [(6^2 - 4) × 2] ÷ 4 + 3", "answer": ((36 - 4) * 2) / 4 + 3},
            {"question": "Evaluate: 4 + 18 ÷ (3 × 3) - 2", "answer": 4 + 18 / 9 - 2},
            {"question": "Simplify: {8 + [3 × (6 - 4)]} × 2", "answer": (8 + (3 * 2)) * 2},

            # Fraction Forest
            {"question": "What is (3/4) + (5/6)? Express in simplest form.", "answer": 19/12},
            {"question": "Simplify: (7/8) ÷ (2/3)", "answer": 21/16},

            # Geometry Gardens
            {"question": "In △ABC (see triangle_diagram.png), AB = AC. If ∠B = 40°, find ∠C.", "answer": 40, "diagram": "assets/grade 7 triangle.png"},  # Isosceles triangle
            {"question": "In circle (see circle_diagram.png), AB is a diameter. Find ∠ACB.", "answer": 90, "diagram": "assets/grade 7 circle.png"},
            {"question": "Find the area of a triangle with base 10 cm and height 8 cm.", "answer": 40, "diagram": "assets/triangle_diagram.png"}
        ],
        "8": [
             # Number Kingdom
             {"question": "Simplify: (4^2 × 3) + 7 - (9 ÷ 3)", "answer": (16 * 3) + 7 - 3},
             {"question": "Evaluate: (3 + 5) × (12 - 4 ÷ 2)", "answer": (3 + 5) * (12 - 2)},
             {"question": "Simplify: [6 × (3^2 + 4)] ÷ 2", "answer": (6 * (9 + 4)) / 2},
             {"question": "What is the value of: (25 - 5^2 + 6 × 2)", "answer": 25 - 25 + 12},
             {"question": "Find the result: 100 ÷ (2 × 5) + 3^2", "answer": 10 + 9},

             # Fraction Forest
             {"question": "What is (5/9) × (3/7)?", "answer": 15/63},
             {"question": "Simplify: (4/5) ÷ (2/3)", "answer": 6/5},

             # Geometry Gardens
             {"question": "In △ABC (see triangle_diagram.png), angle A = 60°, angle B = 80°, find angle C.", "answer": 40,},
             {"question": "Find the radius of a circle (see circle_diagram.png) if diameter is 14 cm.", "answer": 7},
             {"question": "Find the area of a right triangle with legs 6 cm and 8 cm.", "answer": 24}
        ],
        "9": [
             {"question": "Evaluate: [(6^2 - 4^2) × 2] ÷ (2^3) + 5", "answer": ((36 - 16) * 2) / 8 + 5},
             {"question": "Simplify: 5 + (3 × 2^3) - (12 ÷ 4)", "answer": 5 + (3 * 8) - 3},
             {"question": "Evaluate: {18 ÷ (6 - 3)} + (4 × 2^2)", "answer": 6 + 16},
             {"question": "What is the result of: 7^2 - 3 × 4 + 8 ÷ 2", "answer": 49 - 12 + 4},
             {"question": "Solve: (2^4 - 4) ÷ 2 + 5 × 3", "answer": (16 - 4) / 2 + 15},

             {"question": "Evaluate: (9/16) ÷ (3/4)", "answer": 3/4},
             {"question": "Simplify: (7/10) + (2/5)", "answer": 11/10},

             {"question": "In triangle (see triangle_diagram.png), AB = AC and angle B = 70°. Find angle C.", "answer": 70},
             {"question": "Find the angle in a semicircle (see circle_diagram.png).", "answer": 90},
             {"question": "Find the area of a triangle with sides 13 cm, 14 cm, and 15 cm using Heron’s formula.", "answer": 84}
        ],
        "10": [
            # Number Kingdom
            {"question": "Evaluate: [(3^3 + 4^2) - (2^3)] ÷ 5 + 6", "answer": (27 + 16 - 8) / 5 + 6},
            {"question": "Simplify: (8^2 - 4^2) × (3 ÷ 3) + 10", "answer": (64 - 16) * 1 + 10},
            {"question": "Find the value of: [(9 × 3^2) ÷ (27 ÷ 3)] + 2", "answer": (9 * 9) / 9 + 2},
            {"question": "What is (15 - 3)^2 ÷ 6 + 4 × 2?", "answer": 144 / 6 + 8},
            {"question": "Simplify: (2^5 + 3^3) ÷ (7 - 2)", "answer": (32 + 27) / 5},

            {"question": "Simplify: (3/5) × (15/4)", "answer": 9/4},
            {"question": "Evaluate: (11/12) ÷ (11/18)", "answer": 3/2},

            {"question": "In △ABC, AB = AC and angle A = 50°. Find angle B and C.", "answer": 65},
            {"question": "In circle, AB is diameter, CD is chord. Prove angle in semicircle is 90°.", "answer": 90},
            {"question": "Find the area of an equilateral triangle of side 6 cm.", "answer": (3**0.5 / 4) * 36}
        ]
    }
    return problems.get(grade, [])
