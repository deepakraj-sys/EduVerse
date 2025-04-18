"""
This module provides interactive UI components for the EduVerse platform.
"""
import streamlit as st
import time
import random
import pandas as pd
import plotly.express as px
from learning_features import get_quiz_for_module, get_progress_for_module

def display_quiz(module_name, quiz_title, accessibility_manager=None):
    """
    Displays an interactive quiz with accessibility support
    """
    # Get current language and color scheme
    current_language = accessibility_manager.get_current_language() if accessibility_manager else "en"
    color_scheme = accessibility_manager.get_current_color_scheme() if accessibility_manager else None
    screen_reader_enabled = accessibility_manager.is_screen_reader_enabled() if accessibility_manager else False
    """
    Displays an interactive quiz from a module and tracks user's answers.
    
    Args:
        module_name: The name of the module containing the quiz
        quiz_title: The title of the quiz to display
    
    Returns:
        The score achieved in the quiz (0-100)
    """
    quiz = get_quiz_for_module(module_name, quiz_title)
    
    if not quiz:
        st.error(f"Quiz '{quiz_title}' not found for module '{module_name}'")
        return 0
    
    st.subheader(f"📝 {quiz['title']}")
    
    # Create a form for the quiz
    with st.form(key=f"quiz_{module_name}_{quiz_title.replace(' ', '_')}"):
        score = 0
        total_questions = len(quiz['questions'])
        user_answers = {}
        
        for i, question in enumerate(quiz['questions']):
            st.write(f"**Question {i+1}:** {question['question']}")
            
            answer_key = f"q_{i}"
            user_answers[answer_key] = st.radio(
                "Select your answer:",
                question['options'],
                key=f"{module_name}_{quiz_title}_{i}"
            )
            
            st.write("---")
        
        # Submit button for the quiz
        submitted = st.form_submit_button("Submit Answers")
        
        if submitted:
            # Calculate score
            for i, question in enumerate(quiz['questions']):
                if user_answers[f"q_{i}"] == question['answer']:
                    score += 1
            
            score_percentage = (score / total_questions) * 100
            return score_percentage
    
    return None  # Quiz not submitted yet

def display_interactive_lesson(module_name, lesson):
    """
    Displays an interactive lesson with appropriate UI based on content type.
    
    Args:
        module_name: The name of the module containing the lesson
        lesson: The lesson data dictionary
    """
    st.subheader(f"📚 {lesson['title']}")
    st.write(lesson['description'])
    
    # Display lesson metadata
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Difficulty", lesson['difficulty'])
    with col2:
        st.metric("Duration", f"{lesson['duration_minutes']} mins")
    with col3:
        st.metric("Content Type", lesson['content_type'].capitalize())
    
    st.write("**Skills developed:**")
    for skill in lesson['skills']:
        st.write(f"- {skill}")
    
    # Different display based on content type
    if lesson['content_type'] == 'story':
        display_story_content(lesson)
    elif lesson['content_type'] == 'game':
        display_game_content(lesson)
    elif lesson['content_type'] == 'simulation':
        display_simulation_content(lesson)
    elif lesson['content_type'] == 'interactive':
        display_interactive_content(lesson)
    
    # Progress tracking section
    with st.expander("Track Your Progress"):
        progress = get_progress_for_module(module_name)
        if progress:
            lessons_percent = (progress['lessons_completed'] / progress['total_lessons']) * 100
            quizzes_percent = (progress['quizzes_completed'] / progress['total_quizzes']) * 100 if progress['total_quizzes'] > 0 else 0
            
            st.write("**Module Progress:**")
            st.progress(lessons_percent / 100)
            st.write(f"Lessons Completed: {progress['lessons_completed']}/{progress['total_lessons']}")
            
            st.write("**Quiz Progress:**")
            st.progress(quizzes_percent / 100)
            st.write(f"Quizzes Completed: {progress['quizzes_completed']}/{progress['total_quizzes']}")
            
            if progress['avg_quiz_score'] > 0:
                st.write(f"Average Quiz Score: {progress['avg_quiz_score']}%")

def display_story_content(lesson):
    """Displays story-based interactive content."""
    st.write("---")
    st.subheader("Interactive Story")
    
    # Simulate an interactive story with choices
    story_text = """
    You are on a journey through an enchanted forest filled with mathematical mysteries.
    As you venture deeper, you encounter a bridge guarded by a friendly troll.
    
    "To cross this bridge," says the troll, "you must solve a riddle!"
    """
    
    st.write(story_text)
    
    # Simple interactive choice
    choice = st.radio(
        "What do you want to do?",
        ["Attempt to solve the riddle", "Try to find another path", "Offer the troll something in exchange"]
    )
    
    if choice == "Attempt to solve the riddle":
        st.write("""
        The troll smiles and presents you with a math problem.
        "If I have 8 apples and give away half, then eat 2, how many do I have left?"
        """)
        
        answer = st.text_input("Your answer:")
        check = st.button("Check Answer")
        
        if check:
            if answer == "2":
                st.success("Correct! The troll lets you pass the bridge.")
                st.balloons()
            else:
                st.error("That's not right. Try again!")
    
    elif choice == "Try to find another path":
        st.write("""
        You decide to look for another way across. After searching, you find a series of 
        stepping stones across the river, but each stone has a number on it.
        You realize you need to step only on stones where the number is a multiple of 3.
        """)
        
        stones = [1, 3, 5, 6, 7, 9, 10, 12, 15]
        selected_stones = st.multiselect("Select the stones to step on (numbers):", stones)
        
        check = st.button("Try to Cross")
        if check:
            correct_stones = [num for num in stones if num % 3 == 0]
            if all(stone in correct_stones for stone in selected_stones) and len(selected_stones) == len(correct_stones):
                st.success("You successfully cross the river!")
                st.balloons()
            else:
                st.error("You slip and fall back to the shore. Try again!")
    
    else:
        st.write("""
        You offer the troll something in exchange for crossing.
        "I'll accept your gift," says the troll, "if you can solve this pattern."
        
        The troll shows you a sequence: 2, 6, 12, 20, ___
        """)
        
        answer = st.text_input("What's the next number in the sequence?")
        check = st.button("Check Answer")
        
        if check:
            if answer == "30":
                st.success("Correct! The troll accepts your offering and lets you pass.")
                st.balloons()
            else:
                st.error("That's not right. The troll shakes his head. Try again!")

def display_game_content(lesson):
    """Displays game-based interactive content."""
    st.write("---")
    st.subheader("Math Game")
    
    if lesson['title'] == "Fraction Kingdom":
        st.write("""
        Welcome to the Fraction Kingdom! Here, you'll solve fraction problems
        to help the royal mathematicians.
        """)
        
        # Simple fraction comparison game
        st.write("**Fraction Comparison Challenge**")
        st.write("Which fraction is larger? Select your answer.")
        
        # Generate random fractions for comparison
        if 'fraction_game_state' not in st.session_state:
            st.session_state.fraction_game_state = {
                'score': 0,
                'questions': 0,
                'current_question': None
            }
        
        # Generate fractions if not already generated
        if st.session_state.fraction_game_state['current_question'] is None:
            num1, den1 = random.randint(1, 10), random.randint(2, 10)
            num2, den2 = random.randint(1, 10), random.randint(2, 10)
            st.session_state.fraction_game_state['current_question'] = {
                'fraction1': f"{num1}/{den1}",
                'fraction2': f"{num2}/{den2}",
                'answer': 'fraction1' if (num1/den1) > (num2/den2) else 'fraction2'
            }
        
        q = st.session_state.fraction_game_state['current_question']
        
        col1, col2 = st.columns(2)
        with col1:
            fraction1_button = st.button(q['fraction1'])
        with col2:
            fraction2_button = st.button(q['fraction2'])
        
        if fraction1_button or fraction2_button:
            user_answer = 'fraction1' if fraction1_button else 'fraction2'
            if user_answer == q['answer']:
                st.success("Correct!")
                st.session_state.fraction_game_state['score'] += 1
            else:
                st.error("Incorrect!")
            
            st.session_state.fraction_game_state['questions'] += 1
            
            # Generate new question for next round
            num1, den1 = random.randint(1, 10), random.randint(2, 10)
            num2, den2 = random.randint(1, 10), random.randint(2, 10)
            st.session_state.fraction_game_state['current_question'] = {
                'fraction1': f"{num1}/{den1}",
                'fraction2': f"{num2}/{den2}",
                'answer': 'fraction1' if (num1/den1) > (num2/den2) else 'fraction2'
            }
            
            # Display current score
            st.write(f"Score: {st.session_state.fraction_game_state['score']}/{st.session_state.fraction_game_state['questions']}")
            
            # Option to restart
            if st.session_state.fraction_game_state['questions'] >= 5:
                st.write("Game complete!")
                restart = st.button("Play Again")
                if restart:
                    st.session_state.fraction_game_state = {
                        'score': 0,
                        'questions': 0,
                        'current_question': None
                    }
                    st.rerun()

    elif lesson['title'] == "Multiplication Mountain":
        st.write("""
        Welcome to Multiplication Mountain! Solve multiplication problems
        to climb to the peak.
        """)
        
        # Initialize game state
        if 'mult_game_state' not in st.session_state:
            st.session_state.mult_game_state = {
                'level': 1,
                'score': 0,
                'max_level': 5,
                'current_problem': None
            }
        
        # Generate problem if not already generated
        if st.session_state.mult_game_state['current_problem'] is None:
            level = st.session_state.mult_game_state['level']
            num1 = random.randint(1, level * 2)
            num2 = random.randint(1, level * 2)
            st.session_state.mult_game_state['current_problem'] = {
                'num1': num1,
                'num2': num2,
                'answer': num1 * num2
            }
        
        p = st.session_state.mult_game_state['current_problem']
        
        # Display current level
        st.progress(st.session_state.mult_game_state['level'] / st.session_state.mult_game_state['max_level'])
        st.write(f"Level: {st.session_state.mult_game_state['level']}/{st.session_state.mult_game_state['max_level']}")
        st.write(f"Score: {st.session_state.mult_game_state['score']}")
        
        # Display problem
        st.write(f"**Problem:** {p['num1']} × {p['num2']} = ?")
        
        # Get user answer
        user_answer = st.text_input("Your answer:", key="mult_answer")
        check = st.button("Submit Answer")
        
        if check:
            try:
                answer = int(user_answer)
                if answer == p['answer']:
                    st.success("Correct!")
                    st.session_state.mult_game_state['score'] += 10 * st.session_state.mult_game_state['level']
                    
                    # Level up if not at max level
                    if st.session_state.mult_game_state['level'] < st.session_state.mult_game_state['max_level']:
                        st.session_state.mult_game_state['level'] += 1
                    
                    # Generate new problem for next round
                    level = st.session_state.mult_game_state['level']
                    num1 = random.randint(1, level * 2)
                    num2 = random.randint(1, level * 2)
                    st.session_state.mult_game_state['current_problem'] = {
                        'num1': num1,
                        'num2': num2,
                        'answer': num1 * num2
                    }
                    
                    if st.session_state.mult_game_state['level'] == st.session_state.mult_game_state['max_level']:
                        st.balloons()
                        st.write("Congratulations! You've reached the peak of Multiplication Mountain!")
                else:
                    st.error("Incorrect. Try again!")
            except ValueError:
                st.error("Please enter a valid number.")

def display_simulation_content(lesson):
    """Displays simulation-based interactive content."""
    st.write("---")
    st.subheader("Interactive Simulation")
    
    if "Phishing Detection" in lesson['title']:
        st.write("""
        In this simulation, you'll learn to identify phishing attempts in emails.
        Review the example emails below and determine which ones are legitimate
        and which are phishing attempts.
        """)
        
        # Phishing email examples
        emails = [
            {
                "sender": "support@amazen.com",
                "subject": "URGENT: Your Account Will Be Suspended",
                "body": """
                Dear Valued Customer,
                
                We've detected suspicious activity on your account. Your account will be suspended
                within 24 hours unless you verify your information by clicking the link below:
                
                [VERIFY ACCOUNT NOW]
                
                Regards,
                Amazen Support Team
                """,
                "is_phishing": True,
                "clues": [
                    "Urgent language creating pressure",
                    "Slightly misspelled domain (amazen vs amazon)",
                    "Generic greeting instead of your name",
                    "Threatening consequences for inaction"
                ]
            },
            {
                "sender": "notifications@yourbank.com",
                "subject": "Your Monthly Statement Is Ready",
                "body": """
                Hello Alex,
                
                Your January 2025 bank statement is now available in your online banking portal.
                
                To view your statement, please log in to your account through our official website
                at www.yourbank.com or through our mobile app.
                
                Thank you for banking with us.
                
                Sincerely,
                YourBank Customer Service
                """,
                "is_phishing": False,
                "clues": [
                    "Personalized greeting",
                    "No links to click in email body",
                    "Directs to official website login",
                    "No urgent language or threats",
                    "No request for personal information"
                ]
            }
        ]
        
        # Display email and let user determine if it's phishing
        if 'phishing_index' not in st.session_state:
            st.session_state.phishing_index = 0
            st.session_state.phishing_score = 0
            st.session_state.phishing_total = 0
        
        if st.session_state.phishing_index < len(emails):
            email = emails[st.session_state.phishing_index]
            
            with st.container():
                st.markdown("### Email Preview")
                st.markdown(f"**From:** {email['sender']}")
                st.markdown(f"**Subject:** {email['subject']}")
                st.markdown(f"**Body:**\n{email['body']}")
            
            col1, col2 = st.columns(2)
            with col1:
                phishing_button = st.button("This is phishing")
            with col2:
                legitimate_button = st.button("This is legitimate")
            
            if phishing_button or legitimate_button:
                user_answer = phishing_button
                if (user_answer and email['is_phishing']) or (not user_answer and not email['is_phishing']):
                    st.success("Correct identification!")
                    st.session_state.phishing_score += 1
                else:
                    st.error("Incorrect identification!")
                
                # Show explanation
                st.write("### Explanation")
                if email['is_phishing']:
                    st.warning("This is a phishing attempt.")
                    st.write("Red flags to look for:")
                else:
                    st.info("This is a legitimate email.")
                    st.write("Signs that indicate this is legitimate:")
                
                for clue in email['clues']:
                    st.write(f"- {clue}")
                
                st.session_state.phishing_total += 1
                
                # Move to next email
                next_button = st.button("Next Email")
                if next_button:
                    st.session_state.phishing_index += 1
                    st.rerun()
        else:
            # End of simulation
            score_percentage = (st.session_state.phishing_score / st.session_state.phishing_total) * 100
            st.write(f"### Simulation Complete!")
            st.write(f"Your score: {st.session_state.phishing_score}/{st.session_state.phishing_total} ({score_percentage:.1f}%)")
            
            if score_percentage >= 80:
                st.success("Great job! You show strong phishing detection skills.")
            elif score_percentage >= 50:
                st.warning("Good effort, but you should review the phishing indicators again.")
            else:
                st.error("You need more practice to identify phishing attempts.")
            
            # Option to restart
            restart = st.button("Restart Simulation")
            if restart:
                st.session_state.phishing_index = 0
                st.session_state.phishing_score = 0
                st.session_state.phishing_total = 0
                st.rerun()
            
    elif "Circulatory System" in lesson['title']:
        st.write("""
        In this simulation, you'll build a functioning model of the human circulatory system.
        Arrange the components correctly to create a working system.
        """)
        
        # Circulatory system components
        components = [
            "Heart", "Lungs", "Arteries", "Veins", "Capillaries", "Blood Cells"
        ]
        
        # Simulation interface
        st.write("### Circulatory System Components")
        st.write("Drag and arrange the components in the correct order:")
        
        # Since we can't actually do drag and drop in Streamlit, we'll simulate with selectbox
        ordered_components = []
        for i in range(len(components)):
            # Get remaining components
            remaining = [c for c in components if c not in ordered_components]
            if remaining:
                selection = st.selectbox(f"Position {i+1}", remaining, key=f"circ_comp_{i}")
                ordered_components.append(selection)
        
        # Check the arrangement
        correct_order = ["Heart", "Arteries", "Capillaries", "Veins", "Heart", "Lungs"]
        check_arrangement = st.button("Check Arrangement")
        
        if check_arrangement:
            # Check if the length of ordered components is sufficient for comparison
            if len(ordered_components) >= len(correct_order):
                is_correct = all(a == b for a, b in zip(ordered_components[:len(correct_order)], correct_order))
                if is_correct:
                    st.success("Correct! You've built a functioning circulatory system model.")
                    
                    # Display a simple diagram
                    st.write("### Your Circulatory System Model")
                    
                    # Create diagram data
                    diagram_data = pd.DataFrame({
                        'Component': ordered_components[:len(correct_order)],
                        'Position': list(range(1, len(correct_order) + 1)),
                        'Blood Flow': [100, 90, 80, 70, 60, 50]  # Just for visualization
                    })
                    
                    # Create a simple flow diagram
                    fig = px.line(diagram_data, x='Position', y='Blood Flow', 
                              hover_data=['Component'], markers=True,
                              title="Blood Flow Through the Circulatory System")
                    st.plotly_chart(fig)
                    
                    # Explanation
                    st.write("""
                    **How the circulatory system works:**
                    1. The heart pumps oxygen-poor blood to the lungs
                    2. The lungs oxygenate the blood
                    3. The heart pumps oxygen-rich blood through arteries
                    4. Arteries branch into capillaries where oxygen and nutrients are delivered to tissues
                    5. Capillaries merge into veins which return oxygen-poor blood back to the heart
                    6. The cycle repeats
                    """)
                else:
                    st.error("Not quite right. The blood flow wouldn't circulate properly with this arrangement.")
                    st.write("Hint: Consider how blood needs to flow through the system and where oxygenation occurs.")
            else:
                st.warning("Please complete the arrangement before checking.")

def display_interactive_content(lesson):
    """Displays other types of interactive content."""
    st.write("---")
    st.subheader("Interactive Learning")
    
    if "Password Fortresses" in lesson['title']:
        st.write("""
        In this interactive exercise, you'll learn how to create strong passwords
        and understand different authentication methods.
        """)
        
        # Password strength checker
        st.write("### Password Strength Checker")
        st.write("Enter a password to check its strength:")
        
        password = st.text_input("Password", type="password")
        check_strength = st.button("Check Strength")
        
        if check_strength and password:
            # Simple password strength rules
            strength = 0
            feedback = []
            
            # Length check
            if len(password) >= 12:
                strength += 25
                feedback.append("✅ Good length (12+ characters)")
            elif len(password) >= 8:
                strength += 15
                feedback.append("⚠️ Acceptable length (8+ characters)")
            else:
                feedback.append("❌ Too short (less than 8 characters)")
            
            # Uppercase check
            if any(c.isupper() for c in password):
                strength += 25
                feedback.append("✅ Contains uppercase letters")
            else:
                feedback.append("❌ Missing uppercase letters")
            
            # Number check
            if any(c.isdigit() for c in password):
                strength += 25
                feedback.append("✅ Contains numbers")
            else:
                feedback.append("❌ Missing numbers")
            
            # Special character check
            special_chars = "!@#$%^&*()-_=+[]{}|;:'\",.<>/?"
            if any(c in special_chars for c in password):
                strength += 25
                feedback.append("✅ Contains special characters")
            else:
                feedback.append("❌ Missing special characters")
            
            # Display strength
            st.progress(strength / 100)
            
            if strength >= 90:
                st.success(f"Password Strength: Strong ({strength}%)")
            elif strength >= 70:
                st.warning(f"Password Strength: Moderate ({strength}%)")
            else:
                st.error(f"Password Strength: Weak ({strength}%)")
            
            # Display feedback
            st.write("### Password Analysis")
            for item in feedback:
                st.write(item)
            
            # Common password mistakes
            if len(password) >= 4:
                common_patterns = ["1234", "qwerty", "password", "admin", "letmein"]
                for pattern in common_patterns:
                    if pattern.lower() in password.lower():
                        st.error(f"⚠️ Your password contains a common pattern: '{pattern}'")
        
        # Authentication methods
        st.write("### Authentication Methods")
        st.write("""
        Modern security often uses multi-factor authentication, combining:
        
        1. **Something you know** (password, PIN)
        2. **Something you have** (phone, security key)
        3. **Something you are** (fingerprint, face scan)
        """)
        
        auth_method = st.radio(
            "Which authentication method provides the strongest security?",
            [
                "A complex password",
                "A password + SMS code",
                "A password + authenticator app",
                "A password + biometric + security key"
            ]
        )
        
        check_auth = st.button("Check Answer")
        
        if check_auth:
            if auth_method == "A password + biometric + security key":
                st.success("Correct! This combines all three factors for the strongest security.")
            else:
                st.error("Not quite. Multi-factor authentication using all three factors provides the strongest security.")

def display_learning_path_progress(path_name):
    """
    Displays a visual representation of progress through a learning path.
    
    Args:
        path_name: The name of the learning path to display
    """
    from learning_features import get_learning_path_by_name, get_progress_for_module
    
    path = get_learning_path_by_name(path_name)
    if not path:
        st.error(f"Learning path '{path_name}' not found")
        return
    
    st.subheader(f"📊 Learning Path: {path['name']}")
    st.write(path['description'])
    
    # Path metadata
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Difficulty", path['difficulty'])
    with col2:
        st.metric("Target Age", path['target_age'])
    with col3:
        st.metric("Estimated Duration", f"{path['estimated_duration_hours']} hours")
    
    # Progress for each module in the path
    st.write("### Module Progress")
    
    # Create progress bars for each module
    for module_name in path['modules']:
        progress = get_progress_for_module(module_name)
        if progress:
            # Calculate overall module completion percentage
            lesson_weight = 0.7  # Lessons are 70% of module weight
            quiz_weight = 0.3    # Quizzes are 30% of module weight
            
            lesson_progress = progress['lessons_completed'] / progress['total_lessons'] if progress['total_lessons'] > 0 else 0
            quiz_progress = progress['quizzes_completed'] / progress['total_quizzes'] if progress['total_quizzes'] > 0 else 0
            
            overall_progress = (lesson_progress * lesson_weight) + (quiz_progress * quiz_weight)
            
            # Display progress bar
            st.write(f"**{module_name}**")
            st.progress(overall_progress)
            
            # Display progress breakdown
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"Lessons: {progress['lessons_completed']}/{progress['total_lessons']}")
            with col2:
                st.write(f"Quizzes: {progress['quizzes_completed']}/{progress['total_quizzes']}")
            
            if progress['avg_quiz_score'] > 0:
                st.write(f"Quiz Score: {progress['avg_quiz_score']}%")
            
            st.write("---")