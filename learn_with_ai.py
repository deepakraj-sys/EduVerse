import streamlit as st
import PyPDF2
from pytube import YouTube
import google.generativeai as genai
from PIL import Image
import base64
from io import BytesIO

# ----------------- CONFIG ------------------
st.set_page_config(page_title="📚 Learn with AI", layout="wide")
st.markdown("""
    <style>
    .big-title { font-size: 50px !important; font-weight: 800; text-align: center; color: #6C63FF; }
    .subtext { font-size: 18px; text-align: center; color: #555; margin-bottom: 30px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='big-title'>🎓 Learn with AI</div>", unsafe_allow_html=True)
st.markdown("<div class='subtext'>Generate Smart Notes, Flashcards, Quizzes, and More Instantly using Gemini 1.5 Flash</div>", unsafe_allow_html=True)

# ----------------- API INIT ------------------
GEMINI_API_KEY = "AIzaSyBCpPpvrn-Ht8FHwV0omLnk9xsTWEJ_z34"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-flash")

# ----------------- HELPERS ------------------
def extract_pdf_text(uploaded_file):
    text = ""
    reader = PyPDF2.PdfReader(uploaded_file)
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_youtube_transcript(video_url):
    try:
        yt = YouTube(video_url)
        caption = yt.captions.get_by_language_code("en")
        if caption:
            return caption.xml_caption_to_srt()
        else:
            return "No English captions found for this video."
    except Exception as e:
        return f"Error extracting transcript: {str(e)}"

def gemini_generate(content, task, subject):
    task_prompts = {
        "notes": f"You are an expert {subject} teacher. Summarize the following content into structured study notes:\n\n{content}",
        "flashcards": f"Create spaced repetition flashcards from this {subject} content. Include definitions, examples, and formulas where relevant:\n\n{content}",
        "quiz": f"Generate 5 MCQs, 2 True/False, and 2 Short Answer questions for {subject} based on:\n\n{content}",
        "outline": f"Extract a structured outline of key topics and subtopics from the following {subject} content:\n\n{content}",
        "visual_flashcards": f"Extract 3 key flashcard topics from this {subject} content. For each one, include a short description and a visual concept that can be illustrated as an image.\n\n{content}"
    }
    response = model.generate_content(task_prompts[task])
    return response.text

def generate_image(prompt):
    # Placeholder image (you can replace this with actual image generation)
    img = Image.new("RGB", (400, 200), color="lightblue")
    return img

def image_to_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# ----------------- SIDEBAR INPUT ------------------
st.sidebar.header("📥 Input Source")

subject = st.sidebar.selectbox("Select Subject Area:", ["Maths", "Computer", "Engineering", "Chemistry"])
input_type = st.sidebar.selectbox("Choose input type:", ["Text", "PDF", "YouTube Video"])

user_input = ""

if input_type == "Text":
    user_input = st.text_area("Paste your learning content:", height=200)
elif input_type == "PDF":
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
    if uploaded_file:
        user_input = extract_pdf_text(uploaded_file)
elif input_type == "YouTube Video":
    video_url = st.text_input("Paste YouTube video URL:")
    if video_url:
        transcript = extract_youtube_transcript(video_url)
        if transcript.startswith("Error") or "No English captions" in transcript:
            st.error(transcript)
        else:
            user_input = transcript

# ----------------- MAIN BUTTONS ------------------
if user_input:
    st.markdown(f"#### Subject: **{subject}**")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📝 Generate Notes"):
            with st.spinner("Generating notes..."):
                notes = gemini_generate(user_input, "notes", subject)
                st.subheader("🧠 AI-Generated Notes")
                st.write(notes)
    with col2:
        if st.button("📇 Generate Flashcards"):
            with st.spinner("Generating flashcards..."):
                flashcards = gemini_generate(user_input, "flashcards", subject)
                st.subheader("🧠 Flashcards")
                st.write(flashcards)
    with col3:
        if st.button("🧪 Generate Quiz"):
            with st.spinner("Generating quiz..."):
                quiz = gemini_generate(user_input, "quiz", subject)
                st.subheader("🧠 Quiz")
                st.write(quiz)

    # 📂 Topic Outline
    if st.button("📂 Generate Topic Outline"):
        with st.spinner("Extracting outline..."):
            outline = gemini_generate(user_input, "outline", subject)
            st.subheader("📂 Structured Outline")
            st.write(outline)

    # 🎴 Visual Flashcards
    if st.button("🎴 Visual Flashcards"):
        with st.spinner("Generating visual flashcards..."):
            flashcard_data = gemini_generate(user_input, "visual_flashcards", subject)
            st.subheader("🎴 Visual Flashcards")

            # Expecting format: Topic: ..., Description: ..., Visual: ...
            cards = flashcard_data.strip().split("\n\n")
            for i, card in enumerate(cards, start=1):
                lines = card.split("\n")
                title = description = visual_prompt = ""
                for line in lines:
                    if "topic" in line.lower():
                        title = line.split(":", 1)[-1].strip()
                    elif "description" in line.lower():
                        description = line.split(":", 1)[-1].strip()
                    elif "visual" in line.lower():
                        visual_prompt = line.split(":", 1)[-1].strip()

                st.markdown(f"**Flashcard {i}: {title}**")
                st.write(description)
                image = generate_image(visual_prompt or title)
                if image:
                    st.image(image, caption=title, use_column_width=True)

    # 🎯 Real-Time Quiz
    if st.button("🧠 Start Real-Time Quiz"):
        with st.spinner("Generating interactive quiz..."):
            quiz_text = gemini_generate(user_input, "quiz", subject)
            st.session_state.quiz_raw = quiz_text
            st.session_state.current_q = 0
            st.session_state.correct_count = 0
            st.session_state.finished = False

# ----------------- REAL-TIME QUIZ INTERFACE ------------------
# ----------------- REAL-TIME QUIZ INTERFACE ------------------
if "quiz_raw" in st.session_state and not st.session_state.get("finished", False):
    raw_quiz = st.session_state.quiz_raw

    def parse_questions(raw_text):
        questions = []
        blocks = raw_text.split("\n\n")
        for block in blocks:
            lines = block.strip().split("\n")
            if not lines:
                continue
            question_text = ""
            options = []
            answer = ""
            for line in lines:
                line = line.strip()
                if line.lower().startswith("answer:"):
                    answer = line.split(":", 1)[-1].strip()
                elif line[:2] in ["A)", "B)", "C)", "D)"]:
                    options.append(line)
                elif line[0].isdigit() and '.' in line[:3]:
                    question_text = line
                else:
                    question_text += " " + line
            if question_text:
                questions.append({
                    "question": question_text,
                    "options": options,
                    "answer": answer
                })
        return questions

    quiz_questions = parse_questions(raw_quiz)
    total_qs = len(quiz_questions)

    if st.session_state.current_q < total_qs:
        q = quiz_questions[st.session_state.current_q]
        st.subheader(f"Question {st.session_state.current_q + 1}/{total_qs}")
        st.write(q["question"])
        selected = st.radio("Choose an answer:", q["options"], key=f"q{st.session_state.current_q}")

        if st.button("Submit Answer"):
            if selected:  # Fix for NoneType error
                correct = q["answer"]
                if selected.startswith(correct) or correct in selected:
                    st.success("✅ Correct!")
                    st.session_state.correct_count += 1
                else:
                    st.error(f"❌ Incorrect! Correct answer: {correct}")
                st.session_state.current_q += 1
                st.experimental_rerun()
            else:
                st.warning("Please select an answer before submitting.")
    else:
        st.session_state.finished = True
        st.balloons()
        st.success(f"🎉 Quiz Completed! You scored {st.session_state.correct_count}/{total_qs}")

# ----------------- FOOTER ------------------
st.markdown("---")
st.caption("Built with 💡 using Gemini 1.5 Flash and Streamlit")