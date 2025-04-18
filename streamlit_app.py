import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt
import os
from modules_data import (all_modules, get_module_distribution, get_modules_by_category, 
                         get_module_by_name, get_all_categories, get_all_module_names)
from api_integrations import (api_integrations, get_all_api_categories, get_apis_by_category,
                             get_api_by_name, get_api_distribution, get_all_api_names,
                             get_complexity_distribution)
from learning_features import (get_all_learning_modules, get_module_learning_content,
                              get_all_learning_paths, get_learning_path_by_name,
                              get_progress_for_module, get_quiz_for_module,
                              calculate_overall_progress, get_content_type_distribution,
                              get_difficulty_distribution)
from interactive_components import (display_quiz, display_interactive_lesson,
                                  display_learning_path_progress)
# Database imports
from database_models import get_db
from sqlalchemy import func
import database_models as models

# Import new modules
from cybersafe_campus import run_cybersafe_campus
from failure_vault import run_failure_vault
from prived_protocol import run_prived_protocol
from retrofix_garage import run_retrofix_garage
from body_verse_blueprint import run_bodyverse_blueprint
from educational_api_connector import display_api_integration_ui
from skill_sprint import run_mathquest_land
from ecoschool_sim import run_ecoschool_sim
from parent_pal import run_parent_pal
from edu_quests import run_edu_quests
from debate_dynasty import run_debate_dynasty
from life_quest import run_life_quest
from class_worlds import run_class_worlds
from biodesign_studio import run_biodesign_studio
from play_tory import run_playtory
from young_changemakers import show_young_changemakers
from parent_teacher_portal import run_parent_teacher_portal

# Configure the page
st.set_page_config(
    page_title="EduVerse Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar navigation
st.sidebar.header("Navigation")
section = st.sidebar.radio(
    "Select a section:",
    ["Overview", "Module Explorer", "ParentPal", "MathQuest Land", 
     "EcoSchool Sim", "YoungChangemakers", "EduQuests", 
     "Debate Dynasty", "Life Quest", "ClassWorlds", "API Integrations",
     "CyberSafe Campus", "PrivEd Protocol", "Educational API Resources", 
     "BodyVerse Blueprint", "BioDesign Studio", "CivilVerse", "Failure Vault",
     "Parent Teacher Portal", "Learning Paths", "RetroFix Garage"]
)

# Overview section
if section == "Overview":
    st.header("🎓 EduVerse Overview")

    st.write("""
    EduVerse is a comprehensive modular learning ecosystem designed to provide
    innovative educational experiences across various disciplines. The platform
    offers specialized modules targeting K-12 education, cybersecurity, and
    engineering disciplines, with integration capabilities for numerous educational APIs.
    """)

    # Display module distribution chart
    st.subheader("Module Distribution by Category")

    distribution = get_module_distribution()
    df_distribution = pd.DataFrame({
        "Category": distribution["categories"],
        "Number of Modules": distribution["counts"]
    })

    chart = alt.Chart(df_distribution).mark_bar().encode(
        x=alt.X('Category', sort='-y'),
        y='Number of Modules',
        color=alt.Color('Category', scale=alt.Scale(scheme='category10'))
    ).properties(
        height=400
    )

    st.altair_chart(chart, use_container_width=True)

    # Display API integration distribution
    st.subheader("API Integration Categories")

    api_dist = get_api_distribution()
    df_api_dist = pd.DataFrame({
        "Category": api_dist["categories"],
        "Number of APIs": api_dist["counts"]
    })

    api_chart = px.pie(
        df_api_dist, 
        values="Number of APIs", 
        names="Category",
        title="API Distribution by Category",
        color_discrete_sequence=px.colors.qualitative.Safe
    )

    st.plotly_chart(api_chart, use_container_width=True)

    # Technology stack
    st.subheader("Technology Stack")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Web Framework**")
        st.write("Django/Flask for backend development")

        st.markdown("**Frontend Integration**")
        st.write("React/Vue.js for dynamic user interfaces")

        st.markdown("**Database**")
        st.write("Supabase for managing user data and content")

    with col2:
        st.markdown("**Authentication**")
        st.write("Supabase/PyAuth for secure user authentication")

        st.markdown("**API Consumption**")
        st.write("Python's requests library for external API interaction")

        st.markdown("**Gamification**")
        st.write("Pygame or Unity integration for advanced features")

# Module Explorer section
elif section == "Module Explorer":
    st.header("📚 Module Explorer")

    tab1, tab2 = st.tabs(["Browse by Category", "Search Modules"])

    with tab1:
        # Category selection
        category = st.selectbox(
            "Select a module category",
            get_all_categories()
        )

        # Display modules in the selected category
        st.subheader(f"Modules in {category}")

        modules = get_modules_by_category(category)

        for i, module in enumerate(modules):
            with st.expander(f"{module['name']} - {module['age_range']}"):
                st.markdown(f"**Description:** {module['description']}")

                st.markdown("**Key Features:**")
                for feature in module['features']:
                    st.markdown(f"- {feature}")

    with tab2:
        # Search by module name
        module_name = st.selectbox(
            "Select a module",
            get_all_module_names()
        )

        module = get_module_by_name(module_name)

        if module:
            st.subheader(module['name'])
            st.markdown(f"**Category:** {module['category']}")
            st.markdown(f"**Age Range:** {module['age_range']}")
            st.markdown(f"**Description:** {module['description']}")

            st.markdown("**Key Features:**")
            for feature in module['features']:
                st.markdown(f"- {feature}")
        else:
            st.error("Module not found. Please select a valid module name.")

# API Integrations section
elif section == "API Integrations":
    st.header("🔌 API Integrations")

    st.write("""
    EduVerse integrates with various free public APIs to enhance its functionality
    and provide rich educational experiences. Explore the available API integrations below.
    """)

    tab1, tab2, tab3 = st.tabs(["Browse by Category", "Search APIs", "Implementation Complexity"])

    with tab1:
        # Category selection
        api_category = st.selectbox(
            "Select an API category",
            get_all_api_categories()
        )

        # Display APIs in the selected category
        st.subheader(f"APIs in {api_category}")

        apis = get_apis_by_category(api_category)

        for api in apis:
            with st.expander(api['name']):
                st.markdown(f"**Description:** {api['description']}")

                st.markdown("**Use Cases:**")
                for use_case in api['use_cases']:
                    st.markdown(f"- {use_case}")

                st.markdown(f"**Implementation Complexity:** {api['implementation_complexity']}")
                st.markdown(f"**Documentation:** [Link]({api['documentation_url']})")

    with tab2:
        # Search by API name
        api_name = st.selectbox(
            "Select an API",
            get_all_api_names()
        )

        api = get_api_by_name(api_name)

        if api:
            st.subheader(api['name'])
            st.markdown(f"**Category:** {api['category']}")
            st.markdown(f"**Description:** {api['description']}")

            st.markdown("**Use Cases:**")
            for use_case in api['use_cases']:
                st.markdown(f"- {use_case}")

            st.markdown(f"**Implementation Complexity:** {api['implementation_complexity']}")
            st.markdown(f"**Documentation:** [Link]({api['documentation_url']})")
        else:
            st.error("API not found. Please select a valid API name.")

    with tab3:
        # Display API complexity distribution
        st.subheader("API Implementation Complexity")

        complexity = get_complexity_distribution()
        df_complexity = pd.DataFrame({
            "Complexity": complexity["complexities"],
            "Number of APIs": complexity["counts"]
        })

        complexity_chart = px.bar(
            df_complexity,
            x="Complexity",
            y="Number of APIs",
            color="Complexity",
            color_discrete_map={
                "Low": "#4CAF50",
                "Medium": "#FFC107",
                "High": "#F44336"
            }
        )

        st.plotly_chart(complexity_chart, use_container_width=True)

        # Implementation notes
        st.markdown("### Implementation Notes")
        st.write("""
        When integrating these APIs, consider the following:

        - **Low complexity**: Typically requires basic HTTP requests and simple response parsing.
        - **Medium complexity**: May involve authentication, pagination, or more complex data structures.
        - **High complexity**: Requires complex authentication, webhook implementations, or extensive data processing.

        All API integrations should implement proper error handling, rate limiting consideration, and caching where appropriate.
        """)

# Learning Hub section
elif section == "Learning Hub":
    st.header("📖 Learning Hub")

    st.write("""
    Welcome to the EduVerse Learning Hub! This is where you can access interactive
    lessons and quizzes across our educational modules. Choose a module to begin learning.
    """)

    # Overall learning progress
    overall_progress = calculate_overall_progress()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Lesson Progress", f"{overall_progress['lessons_progress']:.1f}%")
    with col2:
        st.metric("Quiz Progress", f"{overall_progress['quizzes_progress']:.1f}%")
    with col3:
        st.metric("Average Quiz Score", f"{overall_progress['avg_quiz_score']:.1f}%")

    # Content type distribution
    st.subheader("Learning Content Types")

    content_dist = get_content_type_distribution()
    df_content = pd.DataFrame({
        "Content Type": content_dist["types"],
        "Number of Lessons": content_dist["counts"]
    })

    content_chart = px.pie(
        df_content,
        values="Number of Lessons",
        names="Content Type",
        title="Content Type Distribution",
        color_discrete_sequence=px.colors.qualitative.Bold
    )

    st.plotly_chart(content_chart, use_container_width=True)

    # Difficulty distribution
    st.subheader("Content Difficulty Distribution")

    difficulty_dist = get_difficulty_distribution()
    df_difficulty = pd.DataFrame({
        "Difficulty": difficulty_dist["levels"],
        "Number of Lessons": difficulty_dist["counts"]
    })

    difficulty_chart = px.bar(
        df_difficulty,
        x="Difficulty",
        y="Number of Lessons",
        color="Difficulty",
        title="Content by Difficulty Level",
        color_discrete_map={
            "Beginner": "#4CAF50",
            "Intermediate": "#FFC107",
            "Advanced": "#F44336"
        }
    )

    st.plotly_chart(difficulty_chart, use_container_width=True)

    # Module selection for lessons
    st.subheader("📚 Interactive Learning Modules")

    learning_module = st.selectbox(
        "Select a module to start learning",
        get_all_learning_modules()
    )

    # Display module content
    module_content = get_module_learning_content(learning_module)

    def is_valid_url(url):
        try:
            return bool(url) and not url.endswith('sample')
        except:
            return False

    if module_content:
        st.write(f"### {learning_module}")
        # Validate video URLs before displaying
        if 'video_url' in module_content:
            if is_valid_url(module_content['video_url']):
                st.video(module_content['video_url'])

        # Tabs for lessons and quizzes
        lesson_tab, quiz_tab = st.tabs(["Lessons", "Quizzes"])

        with lesson_tab:
            st.subheader("Available Lessons")

            if "lessons" in module_content and module_content["lessons"]:
                for i, lesson in enumerate(module_content["lessons"]):
                    with st.expander(f"{i+1}. {lesson['title']} ({lesson['difficulty']})"):
                        st.write(lesson["description"])
                        st.write(f"**Type:** {lesson['content_type'].capitalize()}")
                        st.write(f"**Duration:** {lesson['duration_minutes']} minutes")

                        # Start lesson button
                        start_lesson = st.button(f"Start Lesson", key=f"start_{learning_module}_{i}")

                        if start_lesson:
                            st.session_state.active_lesson = {
                                "module": learning_module,
                                "lesson": lesson
                            }
                            st.rerun()
            else:
                st.write("No lessons available for this module.")

        with quiz_tab:
            st.subheader("Available Quizzes")

            if "quizzes" in module_content and module_content["quizzes"]:
                for i, quiz in enumerate(module_content["quizzes"]):
                    with st.expander(f"{i+1}. {quiz['title']}"):
                        st.write(f"Number of questions: {len(quiz['questions'])}")

                        # Start quiz button
                        start_quiz = st.button(f"Take Quiz", key=f"quiz_{learning_module}_{i}")

                        if start_quiz:
                            st.session_state.active_quiz = {
                                "module": learning_module,
                                "quiz_title": quiz["title"]
                            }
                            st.rerun()
            else:
                st.write("No quizzes available for this module.")

    # Display active lesson if one is selected
    if hasattr(st.session_state, 'active_lesson'):
        st.write("---")
        display_interactive_lesson(
            st.session_state.active_lesson["module"],
            st.session_state.active_lesson["lesson"]
        )

        # Button to return to lesson list
        back_to_lessons = st.button("Back to Lesson List")
        if back_to_lessons:
            del st.session_state.active_lesson
            st.rerun()

    # Display active quiz if one is selected
    if hasattr(st.session_state, 'active_quiz'):
        st.write("---")
        quiz_score = display_quiz(
            st.session_state.active_quiz["module"],
            st.session_state.active_quiz["quiz_title"]
        )

        if quiz_score is not None:  # Quiz was submitted
            st.write(f"### Quiz Results")
            st.write(f"Your score: {quiz_score:.1f}%")

            if quiz_score >= 80:
                st.success("Excellent work! You've mastered this material.")
                st.balloons()
            elif quiz_score >= 60:
                st.warning("Good job! Review the questions you missed to improve your understanding.")
            else:
                st.error("You should review this material and try again.")

            # Button to return to quiz list
            back_to_quizzes = st.button("Back to Quiz List")
            if back_to_quizzes:
                del st.session_state.active_quiz
                st.rerun()

# Learning Paths section
elif section == "Learning Paths":
    st.header("🛤️ Learning Paths")

    st.write("""
    Learning paths provide structured journeys through EduVerse modules,
    helping you develop skills progressively. Choose a learning path to begin.
    """)

    # Display available learning paths
    paths = get_all_learning_paths()

    # Create a column for each path
    cols = st.columns(len(paths))
    selected_path = None

    for i, path in enumerate(paths):
        with cols[i]:
            st.subheader(path["name"])
            st.write(path["description"])
            st.write(f"**Target Age:** {path['target_age']}")
            st.write(f"**Difficulty:** {path['difficulty']}")
            st.write(f"**Duration:** {path['estimated_duration_hours']} hours")

            # Modules included
            st.write("**Included Modules:**")
            for module in path["modules"]:
                st.write(f"- {module}")

            # Select button
            if st.button(f"View Path Details", key=f"view_path_{i}"):
                selected_path = path["name"]

    # Display selected path details
    if selected_path:
        st.write("---")
        display_learning_path_progress(selected_path)

        # Option to enroll in the path
        enroll = st.button("Enroll in this Learning Path")

        if enroll:
            st.success(f"You've enrolled in the {selected_path} learning path!")
            st.info("Start your learning journey by accessing the modules in the Learning Hub.")

# Database Dashboard section
elif section == "Database Dashboard":
    st.header("🗄️ Database Dashboard")

    st.write("""
    This dashboard provides an overview of the EduVerse database system,
    which stores all educational content, user progress, and learning paths.
    """)

    # Get database session
    db = get_db()

    # Database metrics
    st.subheader("Database Metrics")

    # Get record counts from database tables
    categories_count = db.query(func.count(models.Category.id)).scalar() or 0
    modules_count = db.query(func.count(models.Module.id)).scalar() or 0
    lessons_count = db.query(func.count(models.Lesson.id)).scalar() or 0
    quizzes_count = db.query(func.count(models.Quiz.id)).scalar() or 0
    learning_paths_count = db.query(func.count(models.LearningPath.id)).scalar() or 0

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Categories", categories_count)
    with col2:
        st.metric("Modules", modules_count)
    with col3:
        st.metric("Lessons", lessons_count)
    with col4:
        st.metric("Quizzes", quizzes_count) 
    with col5:
        st.metric("Learning Paths", learning_paths_count)

    # Create tabs for database views
    tab1, tab2, tab3, tab4 = st.tabs(["Categories & Modules", "Lessons & Quizzes", "Learning Paths", "Database Management"])

    with tab1:
        st.subheader("Categories and Modules")

        # Display categories
        st.write("### Categories")
        categories = db.query(models.Category).all()
        if categories:
            category_data = []
            for category in categories:
                # Count modules in this category
                module_count = db.query(func.count(models.Module.id)).filter(
                    models.Module.category_id == category.id
                ).scalar() or 0

                category_data.append({
                    "ID": category.id,
                    "Name": category.name,
                    "Description": category.description or "N/A",
                    "Modules Count": module_count
                })

            if category_data:
                st.dataframe(pd.DataFrame(category_data))

                # Visualize category data
                fig = px.bar(
                    pd.DataFrame(category_data),
                    x="Name",
                    y="Modules Count",
                    title="Modules per Category",
                    color="Modules Count",
                    color_continuous_scale=px.colors.sequential.Viridis
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No categories found in the database.")

        # Display modules
        st.write("### Modules")
        modules = db.query(models.Module).all()
        if modules:
            module_data = []
            for module in modules:
                # Get category name
                category = db.query(models.Category).filter(
                    models.Category.id == module.category_id
                ).first()

                category_name = category.name if category else "Unknown"

                # Count lessons and quizzes
                lesson_count = db.query(func.count(models.Lesson.id)).filter(
                    models.Lesson.module_id == module.id
                ).scalar() or 0

                quiz_count = db.query(func.count(models.Quiz.id)).filter(
                    models.Quiz.module_id == module.id
                ).scalar() or 0

                module_data.append({
                    "ID": module.id,
                    "Name": module.name,
                    "Category": category_name,
                    "Age Range": module.age_range,
                    "Lessons": lesson_count,
                    "Quizzes": quiz_count
                })

            if module_data:
                st.dataframe(pd.DataFrame(module_data))
        else:
            st.info("No modules found in the database.")

    with tab2:
        st.subheader("Lessons and Quizzes")

        # Display lessons
        st.write("### Lessons")
        lessons = db.query(models.Lesson).all()
        if lessons:
            lesson_data = []
            for lesson in lessons:
                # Get module name
                module = db.query(models.Module).filter(
                    models.Module.id == lesson.module_id
                ).first()

                module_name = module.name if module else "Unknown"

                lesson_data.append({
                    "ID": lesson.id,
                    "Title": lesson.title,
                    "Module": module_name,
                    "Content Type": lesson.content_type,
                    "Difficulty": lesson.difficulty,
                    "Duration (min)": lesson.duration_minutes
                })

            if lesson_data:
                st.dataframe(pd.DataFrame(lesson_data))

                # Visualize lesson data by content type
                df_lesson_types = pd.DataFrame(lesson_data)
                lesson_type_counts = df_lesson_types["Content Type"].value_counts().reset_index()
                lesson_type_counts.columns = ["Content Type", "Count"]

                fig = px.pie(
                    lesson_type_counts,
                    values="Count",
                    names="Content Type",
                    title="Lessons by Content Type",
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                st.plotly_chart(fig, use_container_width=True)

                # Visualize lesson data by difficulty
                lesson_difficulty_counts = df_lesson_types["Difficulty"].value_counts().reset_index()
                lesson_difficulty_counts.columns = ["Difficulty", "Count"]

                fig = px.bar(
                    lesson_difficulty_counts,
                    x="Difficulty",
                    y="Count",
                    title="Lessons by Difficulty",
                    color="Difficulty",
                    color_discrete_map={
                        "Beginner": "#4CAF50",
                        "Intermediate": "#FFC107",
                        "Advanced": "#F44336"
                    }
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No lessons found in the database.")

        # Display quizzes
        st.write("### Quizzes")
        quizzes = db.query(models.Quiz).all()
        if quizzes:
            quiz_data = []
            for quiz in quizzes:
                # Get module name
                module = db.query(models.Module).filter(
                    models.Module.id == quiz.module_id
                ).first()

                module_name = module.name if module else "Unknown"

                # Count questions
                question_count = len(quiz.questions) if quiz.questions else 0

                quiz_data.append({
                    "ID": quiz.id,
                    "Title": quiz.title,
                    "Module": module_name,
                    "Questions": question_count
                })

            if quiz_data:
                st.dataframe(pd.DataFrame(quiz_data))
        else:
            st.info("No quizzes found in the database.")

    with tab3:
        st.subheader("Learning Paths")

        # Display learning paths
        learning_paths = db.query(models.LearningPath).all()
        if learning_paths:
            path_data = []
            for path in learning_paths:
                # Count modules in path
                module_count = len(path.modules) if path.modules else 0

                path_data.append({
                    "ID": path.id,
                    "Name": path.name,
                    "Target Age": path.target_age,
                    "Difficulty": path.difficulty,
                    "Duration (hours)": path.estimated_duration_hours,
                    "Module Count": module_count
                })

            if path_data:
                st.dataframe(pd.DataFrame(path_data))

                # Visualize learning paths by difficulty
                df_paths = pd.DataFrame(path_data)
                path_difficulty_counts = df_paths["Difficulty"].value_counts().reset_index()
                path_difficulty_counts.columns = ["Difficulty", "Count"]

                fig = px.bar(
                    path_difficulty_counts,
                    x="Difficulty",
                    y="Count",
                    title="Learning Paths by Difficulty",
                    color="Difficulty",
                    color_discrete_map={
                        "Beginner": "#4CAF50",
                        "Intermediate": "#FFC107",
                        "Advanced": "#F44336"
                    }
                )
                st.plotly_chart(fig, use_container_width=True)

                # Visualize learning paths by duration
                fig = px.scatter(
                    df_paths,
                    x="Difficulty",
                    y="Duration (hours)",
                    size="Module Count",
                    color="Name",
                    title="Learning Path Duration vs. Difficulty",
                    hover_name="Name"
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No learning paths found in the database.")

    with tab4:
        st.subheader("Database Management")

        st.write("""
        This section provides tools for database management and maintenance.
        Be careful with these operations as they can modify the database.
        """)

        # Database initialization
        st.write("### Initialize Database")
        st.write("""
        Populate the database with sample data from the application.
        This will add categories, modules, lessons, quizzes, and learning paths.
        """)

        init_db = st.button("Initialize Database with Sample Data")

        if init_db:
            try:
                # Import and run database initialization
                from db_service import populate_sample_data
                populate_sample_data(db)
                st.success("Database successfully initialized with sample data!")
            except Exception as e:
                st.error(f"Error initializing database: {str(e)}")

# CyberSafe Campus Module
elif section == "CyberSafe Campus":
    # Run the CyberSafe Campus module
    run_cybersafe_campus()

# PrivEd Protocol Module
elif section == "PrivEd Protocol":
    run_prived_protocol()

# RetroFix Garage Module
elif section == "RetroFix Garage":
    # Run the RetroFix Garage module
    run_retrofix_garage()

# BodyVerse Blueprint Module
elif section == "BodyVerse Blueprint":
    # Run the BodyVerse Blueprint module
    run_bodyverse_blueprint()

# Educational API Resources Module
elif section == "MathQuest Land":
    run_mathquest_land()

elif section == "EcoSchool Sim":
    run_ecoschool_sim()

elif section == "ParentPal":
    run_parent_pal()

elif section == "Educational API Resources":
    # Display the Educational API Integration UI
    display_api_integration_ui()

elif section == "EduQuests":
    run_edu_quests()

elif section == "Debate Dynasty":
    run_debate_dynasty()

elif section == "Life Quest":
    run_life_quest()

elif section == "YoungChangemakers":
    show_young_changemakers()

elif section == "ClassWorlds":
    run_class_worlds()

elif section == "BioDesign Studio":
    run_biodesign_studio()

elif section == "Failure Vault":
    run_failure_vault()

elif section == "PlayTory":
    run_playtory()
    
elif section == "Parent Teacher Portal":
    run_parent_teacher_portal()


# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center;">
        <p>EduVerse: Modular Learning Ecosystem Dashboard </p>
    </div>
    """, 
    unsafe_allow_html=True
)
