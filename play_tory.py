def run_playtory():
    import streamlit as st
    import requests
    import pyttsx3
    import speech_recognition as sr
    from fpdf import FPDF
    import google.generativeai as genai
    import pythoncom

    GEMINI_API_KEY = "AIzaSyBbM4ZIGxHIaWtANIwmu-yxLEgJdVZAF7E"
    YOUTUBE_API_KEY = "AIzaSyDPIk654PaVnlX1CICpcAQzuJ9K_2y5oEw"

    openstax_books = [
        {"title": "Prealgebra", "url": "https://openstax.org/books/prealgebra/pages/1-introduction"},
        {"title": "Algebra and Trigonometry", "url": "https://openstax.org/books/algebra-and-trigonometry/pages/1-introduction"},
        {"title": "Biology", "url": "https://openstax.org/books/biology/pages/1-introduction"},
        {"title": "Concepts of Biology", "url": "https://openstax.org/books/concepts-biology/pages/1-introduction"},
        {"title": "College Physics", "url": "https://openstax.org/books/college-physics/pages/1-introduction"},
        {"title": "University Physics Volume 1", "url": "https://openstax.org/books/university-physics-volume-1/pages/1-introduction"},
        {"title": "University Physics Volume 2", "url": "https://openstax.org/books/university-physics-volume-2/pages/1-introduction"},
        {"title": "University Physics Volume 3", "url": "https://openstax.org/books/university-physics-volume-3/pages/1-introduction"},
        {"title": "Chemistry", "url": "https://openstax.org/books/chemistry/pages/1-introduction"},
        {"title": "Introductory Statistics", "url": "https://openstax.org/books/introductory-statistics/pages/1-introduction"},
        {"title": "Economics", "url": "https://openstax.org/books/principles-economics-2e/pages/1-introduction"},
        {"title": "Macroeconomics", "url": "https://openstax.org/books/principles-macroeconomics-2e/pages/1-introduction"},
        {"title": "Microeconomics", "url": "https://openstax.org/books/principles-microeconomics-2e/pages/1-introduction"},
        {"title": "U.S. History", "url": "https://openstax.org/books/us-history/pages/1-introduction"},
        {"title": "World History", "url": "https://openstax.org/books/world-history/pages/1-introduction"},
        {"title": "Psychology", "url": "https://openstax.org/books/psychology-2e/pages/1-introduction"},
        {"title": "Sociology", "url": "https://openstax.org/books/introduction-sociology-3e/pages/1-introduction"},
    ]

    pythoncom.CoInitialize()
    tts_engine = pyttsx3.init()

    def speak(text):
        for chunk in text.split('. '):
            tts_engine.say(chunk)
        tts_engine.runAndWait()

    def listen():
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
            try:
                return recognizer.recognize_google(audio)
            except sr.UnknownValueError:
                return ""

    def fetch_youtube_videos(query):
        search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&key={YOUTUBE_API_KEY}&type=video&maxResults=5"
        try:
            res = requests.get(search_url).json()
            return res.get('items', [])
        except Exception:
            return []

    genai.configure(api_key=GEMINI_API_KEY)

    def generate_story(prompt):
        try:
            model = genai.GenerativeModel("models/gemini-1.5-flash")
            chat = model.start_chat()
            response = chat.send_message(prompt)
            return response.text
        except Exception as e:
            return f"Error generating story: {e}"

    if "progress" not in st.session_state:
        st.session_state.progress = {
            "chapter": 1,
            "points": 0,
            "badges": [],
            "history": []
        }

    def update_progress(decision, story_chunk):
        st.session_state.progress["chapter"] += 1
        st.session_state.progress["points"] += 10
        if decision.lower() in ["correct", "smart", "creative"]:
            st.session_state.progress["badges"].append(f"🏅 Badge {len(st.session_state.progress['badges'])+1}")
        st.session_state.progress["history"].append(story_chunk)

    def export_story_as_pdf(subject):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for chunk in st.session_state.progress["history"]:
            pdf.multi_cell(0, 10, chunk)
            pdf.ln()
        filename = f"{subject.replace(':', '').replace(' ', '_')}_PlayTory_Story.pdf"
        pdf.output(filename)

    st.set_page_config(page_title="PlayTory", layout="wide")
    st.title("📖 PlayTory – Story-Based Subject Learning")

    st.sidebar.header("Your Progress")
    st.sidebar.write(f"**Chapter:** {st.session_state.progress['chapter']}")
    st.sidebar.write(f"**Points:** {st.session_state.progress['points']}")
    st.sidebar.write(f"**Badges:** {' '.join(st.session_state.progress['badges']) or 'No badges yet.'}")

    subjects = [
        "Class 6: Mathematics", "Class 7: Mathematics", "Class 8: Mathematics", "Class 9: Mathematics", "Class 10: Mathematics", 
        "Class 11: Mathematics Part I", "Class 11: Mathematics Part II", "Class 12: Mathematics Part I", "Class 12: Mathematics Part II",
        "Class 6-8: Science", "Class 9: Science", "Class 10: Science", "Class 11: Biology", "Class 12: Biology", 
        "Class 11: Physics Part I", "Class 11: Physics Part II", "Class 12: Physics Part I", "Class 12: Physics Part II",
        "Class 6: History", "Class 6: Geography", "Class 6: Civics",
        "Class 7: History", "Class 7: Geography", "Class 7: Civics",
        "Class 8: History", "Class 8: Geography", "Class 8: Civics",
        "Class 9: History", "Class 9: Geography", "Class 9: Civics", "Class 9: Economics",
        "Class 10: History", "Class 10: Geography", "Class 10: Civics", "Class 10: Economics",
        "Class 11: History", "Class 11: Geography", "Class 11: Political Science", "Class 11: Economics",
        "Class 12: History", "Class 12: Geography", "Class 12: Political Science", "Class 12: Economics"
    ]

    subject = st.selectbox("🎯 Choose your subject to start the adventure:", subjects)

    if st.button("🎮 Start Story"):
        prompt = f"Write a 2000-word choose-your-own-adventure story based on {subject}. Make it educational, story-driven, and engaging. Include learning challenges and interactive decisions."
        story = generate_story(prompt)
        st.session_state.story = story
        update_progress("start", story)

    if "story" in st.session_state:
        st.subheader("🌟 Your Story")
        st.markdown(st.session_state.story)
        speak(st.session_state.story)

        choice = st.text_input("🗺️ What will you do next? (e.g., Solve the problem / Take a risk / Help a friend)")
        if st.button("Submit Choice"):
            next_prompt = f"Continue the educational adventure based on {subject} after the user decides to: {choice}. Include related learning activities."
            new_story = generate_story(next_prompt)
            st.session_state.story = new_story
            update_progress(choice, new_story)
            st.experimental_rerun()

        if st.button("📄 Export Story as PDF"):
            export_story_as_pdf(subject)
            st.success("PDF exported successfully!")

        st.markdown("---")
        st.subheader("🎓 Learn More")

        with st.expander("📚 OpenStax Books"):
            matches = [book for book in openstax_books if any(word in book["title"].lower() for word in subject.lower().split())]
            if matches:
                for match in matches:
                    st.markdown(f"- [{match['title']}]({match['url']})")
            else:
                st.info("No direct OpenStax book match found for this subject.")

        with st.expander("🎥 YouTube Videos"):
            results = fetch_youtube_videos(subject)
            for video in results:
                if 'videoId' in video['id']:
                    video_id = video['id']['videoId']
                    title = video['snippet']['title']
                    st.markdown(f"**{title}**")
                    st.video(f"https://www.youtube.com/watch?v={video_id}")

    st.markdown("---")
    st.caption("Developed with EduVerse")
