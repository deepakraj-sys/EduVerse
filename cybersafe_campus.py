"""
CyberSafe Campus - Security Awareness Simulator for Schools
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import json
import random
import time
import datetime
from typing import List, Dict, Any, Optional
from database_models import get_db
import database_models as models
from sqlalchemy import func

# ------ Data Models & State Management ------

class SimulationScenario:
    def __init__(
        self,
        id: int,
        title: str,
        description: str,
        difficulty: str,
        scenario_type: str,
        content: Dict[str, Any],
        points: int
    ):
        self.id = id
        self.title = title
        self.description = description
        self.difficulty = difficulty
        self.scenario_type = scenario_type
        self.content = content
        self.points = points


class UserProgress:
    def __init__(
        self,
        user_id: int,
        completed_scenarios: List[int],
        current_level: int,
        total_points: int,
        badges: List[str],
        security_score: float,
        high_risk_behaviors: int
    ):
        self.user_id = user_id
        self.completed_scenarios = completed_scenarios
        self.current_level = current_level
        self.total_points = total_points
        self.badges = badges
        self.security_score = security_score
        self.high_risk_behaviors = high_risk_behaviors


# ------ Sample Data ------

def get_sample_scenarios() -> List[SimulationScenario]:
    """Get sample cybersecurity scenarios."""
    return [
        SimulationScenario(
            id=1,
            title="Suspicious Email Alert",
            description="Learn to identify phishing emails by examining suspicious messages.",
            difficulty="Beginner",
            scenario_type="phishing",
            content={
                "email": {
                    "from": "amazon-support@amazn-services.com",
                    "subject": "URGENT: Your Account Will Be Suspended",
                    "body": """
                    Dear Valued Customer,
                    
                    We have detected unusual activity on your account. Your account will be suspended within 24 hours 
                    unless you verify your information by clicking the link below:
                    
                    [VERIFY ACCOUNT NOW]
                    
                    Regards,
                    Amazon Support Team
                    """,
                    "red_flags": [
                        "Slightly misspelled sender domain (amazn-services.com)",
                        "Urgent language creating pressure",
                        "Generic greeting instead of your name",
                        "Request to click on suspicious link"
                    ]
                },
                "questions": [
                    {
                        "question": "Is this email legitimate or a phishing attempt?",
                        "options": ["Legitimate", "Phishing Attempt"],
                        "correct_answer": "Phishing Attempt"
                    },
                    {
                        "question": "What should you do with this email?",
                        "options": [
                            "Click the link to verify",
                            "Reply asking for more information",
                            "Delete it and/or report as phishing",
                            "Forward it to colleagues to warn them"
                        ],
                        "correct_answer": "Delete it and/or report as phishing"
                    },
                    {
                        "question": "Select all the red flags in this email:",
                        "options": [
                            "Misspelled sender domain",
                            "Urgent language",
                            "Generic greeting",
                            "Suspicious link",
                            "Poor formatting",
                            "Request for personal information"
                        ],
                        "correct_answers": [
                            "Misspelled sender domain",
                            "Urgent language",
                            "Generic greeting",
                            "Suspicious link"
                        ],
                        "type": "multi"
                    }
                ]
            },
            points=100
        ),
        SimulationScenario(
            id=2,
            title="Password Strength Challenge",
            description="Learn to create and evaluate secure passwords.",
            difficulty="Beginner",
            scenario_type="password",
            content={
                "instruction": "Create a strong password that meets all security criteria.",
                "password_tasks": [
                    {
                        "task": "Create a password with at least 12 characters, including uppercase, lowercase, numbers, and special characters",
                        "evaluation": {
                            "min_length": 12,
                            "require_uppercase": True,
                            "require_lowercase": True,
                            "require_numbers": True,
                            "require_special": True,
                            "banned_words": ["password", "123456", "qwerty", "admin"]
                        }
                    },
                    {
                        "task": "Evaluate the security of existing passwords",
                        "passwords": [
                            {"password": "password123", "is_secure": False},
                            {"password": "Tr0ub4dor&3", "is_secure": True},
                            {"password": "qwerty12345", "is_secure": False},
                            {"password": "P@$$w0rd2023!", "is_secure": True}
                        ]
                    }
                ],
                "questions": [
                    {
                        "question": "Which of these is a secure password?",
                        "options": [
                            "password123",
                            "Tr0ub4dor&3",
                            "qwerty12345",
                            "birthdate1990"
                        ],
                        "correct_answer": "Tr0ub4dor&3"
                    },
                    {
                        "question": "What makes a password strong?",
                        "options": [
                            "Using your name with some numbers",
                            "Using the same password for all accounts for consistency",
                            "Length, complexity, uniqueness, and randomness",
                            "Words that are easy to remember"
                        ],
                        "correct_answer": "Length, complexity, uniqueness, and randomness"
                    }
                ]
            },
            points=100
        ),
        SimulationScenario(
            id=3,
            title="Social Media Privacy Challenge",
            description="Learn how to secure your social media accounts and manage privacy settings.",
            difficulty="Intermediate",
            scenario_type="social_media",
            content={
                "instruction": "Review and fix the privacy settings for a fictional social media account.",
                "account_setup": {
                    "current_settings": [
                        {"setting": "Profile Visibility", "value": "Public", "recommended": "Friends Only"},
                        {"setting": "Post Visibility", "value": "Public", "recommended": "Friends Only"},
                        {"setting": "Location Sharing", "value": "Always On", "recommended": "Off"},
                        {"setting": "Tag Approval", "value": "Off", "recommended": "On"},
                        {"setting": "App Permissions", "value": "All Access", "recommended": "Limited Access"}
                    ]
                },
                "questions": [
                    {
                        "question": "Which settings should be changed to improve privacy?",
                        "options": [
                            "Only Location Sharing",
                            "Only Profile Visibility",
                            "All of the current settings",
                            "None, the settings are secure"
                        ],
                        "correct_answer": "All of the current settings"
                    },
                    {
                        "question": "Why is it risky to share your location publicly?",
                        "options": [
                            "It's not risky, just a convenience feature",
                            "It could reveal your home or work location to strangers",
                            "It uses too much battery",
                            "It makes your photos less interesting"
                        ],
                        "correct_answer": "It could reveal your home or work location to strangers"
                    }
                ],
                "action_tasks": [
                    {
                        "task": "Select all settings that should be changed",
                        "options": [
                            "Profile Visibility: Public → Friends Only",
                            "Post Visibility: Public → Friends Only",
                            "Location Sharing: Always On → Off",
                            "Tag Approval: Off → On",
                            "App Permissions: All Access → Limited Access"
                        ],
                        "correct_answers": [
                            "Profile Visibility: Public → Friends Only",
                            "Post Visibility: Public → Friends Only",
                            "Location Sharing: Always On → Off",
                            "Tag Approval: Off → On",
                            "App Permissions: All Access → Limited Access"
                        ],
                        "type": "multi"
                    }
                ]
            },
            points=150
        ),
        SimulationScenario(
            id=4,
            title="Public Wi-Fi Security",
            description="Learn the risks of public Wi-Fi and how to protect yourself.",
            difficulty="Intermediate",
            scenario_type="network_security",
            content={
                "scenario": """
                You're at a coffee shop and need to check your bank account balance.
                The coffee shop offers free, open Wi-Fi.
                """,
                "options": [
                    {
                        "action": "Connect directly to the Wi-Fi and log in to your bank account",
                        "is_secure": False,
                        "explanation": "Connecting to open Wi-Fi and accessing sensitive accounts puts your data at risk of interception."
                    },
                    {
                        "action": "Use your phone's cellular data instead of Wi-Fi",
                        "is_secure": True,
                        "explanation": "Cellular data is encrypted and more secure than public Wi-Fi."
                    },
                    {
                        "action": "Connect to the Wi-Fi but use a VPN before logging in",
                        "is_secure": True,
                        "explanation": "A VPN encrypts your traffic, protecting your data even on insecure networks."
                    },
                    {
                        "action": "Ask the barista for the Wi-Fi password first",
                        "is_secure": False,
                        "explanation": "Password-protected Wi-Fi is better than open Wi-Fi, but still not secure enough for banking."
                    }
                ],
                "questions": [
                    {
                        "question": "What makes public Wi-Fi risky?",
                        "options": [
                            "It's usually too slow to be useful",
                            "Your traffic can be intercepted by others on the network",
                            "It damages your device's Wi-Fi antenna",
                            "Public Wi-Fi is not risky if it has a password"
                        ],
                        "correct_answer": "Your traffic can be intercepted by others on the network"
                    },
                    {
                        "question": "Which protection method is most effective on public Wi-Fi?",
                        "options": [
                            "Closing your browser between sessions",
                            "Using private browsing mode",
                            "Using a VPN",
                            "Clearing cookies regularly"
                        ],
                        "correct_answer": "Using a VPN"
                    }
                ]
            },
            points=150
        ),
        SimulationScenario(
            id=5,
            title="Device Security Challenge",
            description="Learn how to secure your personal devices against unauthorized access.",
            difficulty="Advanced",
            scenario_type="device_security",
            content={
                "instruction": "Audit and improve the security of a personal device.",
                "device_status": [
                    {"setting": "Screen Lock", "current": "None", "recommended": "PIN, Pattern, or Biometric"},
                    {"setting": "Software Updates", "current": "3 months outdated", "recommended": "Up to date"},
                    {"setting": "Encryption", "current": "Off", "recommended": "On"},
                    {"setting": "Backup", "current": "None", "recommended": "Regular cloud or local backup"},
                    {"setting": "Find My Device", "current": "Off", "recommended": "On"}
                ],
                "questions": [
                    {
                        "question": "Why is it important to keep your device's software updated?",
                        "options": [
                            "To get new features",
                            "To fix security vulnerabilities",
                            "To improve battery life",
                            "It's not important"
                        ],
                        "correct_answer": "To fix security vulnerabilities"
                    },
                    {
                        "question": "What should you do if your device is lost or stolen?",
                        "options": [
                            "Nothing, it's just bad luck",
                            "Just buy a new one",
                            "Use Find My Device to locate or wipe it and change all passwords",
                            "Only worry if it had important data"
                        ],
                        "correct_answer": "Use Find My Device to locate or wipe it and change all passwords"
                    }
                ],
                "action_tasks": [
                    {
                        "task": "Select all settings that should be fixed",
                        "options": [
                            "Enable Screen Lock",
                            "Update Software",
                            "Enable Encryption",
                            "Set up Regular Backups",
                            "Enable Find My Device"
                        ],
                        "correct_answers": [
                            "Enable Screen Lock",
                            "Update Software",
                            "Enable Encryption",
                            "Set up Regular Backups",
                            "Enable Find My Device"
                        ],
                        "type": "multi"
                    }
                ]
            },
            points=200
        )
    ]


def get_sample_badges() -> List[Dict[str, str]]:
    """Get sample achievement badges."""
    return [
        {
            "id": "phishing_expert",
            "name": "Phishing Expert",
            "description": "Successfully completed all phishing detection challenges",
            "image": "🎣"
        },
        {
            "id": "password_master",
            "name": "Password Master",
            "description": "Mastered the art of strong password creation",
            "image": "🔐"
        },
        {
            "id": "social_guardian",
            "name": "Social Guardian",
            "description": "Expert in social media privacy protection",
            "image": "👥"
        },
        {
            "id": "wifi_warrior",
            "name": "Wi-Fi Warrior",
            "description": "Knows how to stay safe on public networks",
            "image": "📶"
        },
        {
            "id": "device_defender",
            "name": "Device Defender",
            "description": "Mastered device security best practices",
            "image": "📱"
        },
        {
            "id": "security_novice",
            "name": "Security Novice",
            "description": "Completed 5 security scenarios",
            "image": "🔰"
        },
        {
            "id": "security_apprentice",
            "name": "Security Apprentice",
            "description": "Completed 10 security scenarios",
            "image": "🥉"
        },
        {
            "id": "security_adept",
            "name": "Security Adept",
            "description": "Completed 15 security scenarios",
            "image": "🥈"
        },
        {
            "id": "security_expert",
            "name": "Security Expert",
            "description": "Completed all security scenarios",
            "image": "🥇"
        },
        {
            "id": "perfect_score",
            "name": "Perfect Score",
            "description": "Achieved 100% on a security challenge",
            "image": "💯"
        }
    ]


def get_sample_user_progress() -> UserProgress:
    """Get sample user progress data."""
    if 'cybersafe_user_progress' not in st.session_state:
        st.session_state.cybersafe_user_progress = UserProgress(
            user_id=1,
            completed_scenarios=[],
            current_level=1,
            total_points=0,
            badges=[],
            security_score=0.0,
            high_risk_behaviors=0
        )
    return st.session_state.cybersafe_user_progress


def get_sample_class_data() -> List[Dict[str, Any]]:
    """Get sample class data for teacher dashboard."""
    return [
        {"student_id": 1, "name": "Alex Johnson", "grade": "10th", "security_score": 85, "completed_scenarios": 7, "high_risk_behaviors": 2},
        {"student_id": 2, "name": "Jamie Smith", "grade": "10th", "security_score": 92, "completed_scenarios": 9, "high_risk_behaviors": 1},
        {"student_id": 3, "name": "Taylor Brown", "grade": "10th", "security_score": 78, "completed_scenarios": 5, "high_risk_behaviors": 3},
        {"student_id": 4, "name": "Jordan Lee", "grade": "10th", "security_score": 95, "completed_scenarios": 10, "high_risk_behaviors": 0},
        {"student_id": 5, "name": "Casey Wilson", "grade": "10th", "security_score": 70, "completed_scenarios": 4, "high_risk_behaviors": 4},
        {"student_id": 6, "name": "Riley Garcia", "grade": "10th", "security_score": 88, "completed_scenarios": 8, "high_risk_behaviors": 2},
        {"student_id": 7, "name": "Quinn Martinez", "grade": "10th", "security_score": 75, "completed_scenarios": 6, "high_risk_behaviors": 3},
        {"student_id": 8, "name": "Avery Robinson", "grade": "10th", "security_score": 90, "completed_scenarios": 8, "high_risk_behaviors": 1},
        {"student_id": 9, "name": "Morgan Davis", "grade": "10th", "security_score": 82, "completed_scenarios": 7, "high_risk_behaviors": 2},
        {"student_id": 10, "name": "Drew Miller", "grade": "10th", "security_score": 87, "completed_scenarios": 7, "high_risk_behaviors": 2},
    ]


# ------ UI Components ------

def run_cybersafe_header():
    """Display the header for CyberSafe Campus module."""
    st.markdown(
        """
        <div style="background-color:#2C3E50; padding:10px; border-radius:10px; margin-bottom:10px">
            <h1 style="color:white; text-align:center">
                <span style="font-size:1.5em">🛡️</span> CyberSafe Campus <span style="font-size:1.5em">🛡️</span>
            </h1>
            <h3 style="color:#F4D03F; text-align:center">Security Awareness Simulator for Schools</h3>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_progress_bar(current: int, total: int, label: str = ""):
    """Render a custom progress bar."""
    if total == 0:
        percent = 0
    else:
        percent = min(current / total, 1.0)
    
    # Choose color based on percentage
    if percent >= 0.8:
        color = "#4CAF50"  # Green
    elif percent >= 0.6:
        color = "#FFC107"  # Yellow
    else:
        color = "#F44336"  # Red
    
    st.markdown(
        f"""
        <div style="margin-bottom:10px;">
            <span style="font-weight:bold;">{label}</span>
            <div style="width:100%; background-color:#ddd; border-radius:5px;">
                <div style="width:{percent*100}%; height:20px; background-color:{color}; border-radius:5px; text-align:center; color:white;">
                    {int(percent*100)}%
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_badge(badge: Dict[str, str], earned: bool = False):
    """Render a badge with visual state (earned or locked)."""
    opacity = "1.0" if earned else "0.4"
    locked = "" if earned else "🔒"
    st.markdown(
        f"""
        <div style="display:inline-block; margin:10px; text-align:center; opacity:{opacity}; width:120px; height:120px;">
            <div style="font-size:3em; margin-bottom:5px;">{badge['image']}</div>
            <div style="font-weight:bold;">{badge['name']} {locked}</div>
            <div style="font-size:0.8em;">{badge['description']}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_level_progress(current_level: int, total_points: int):
    """Render level progress indicator."""
    # Calculate points needed for next level
    points_per_level = 500
    points_for_next_level = current_level * points_per_level
    progress_to_next_level = total_points % points_per_level
    percent_to_next = progress_to_next_level / points_per_level
    
    st.markdown(
        f"""
        <div style="background-color:#1E3A8A; padding:15px; border-radius:10px; color:white; margin-bottom:15px;">
            <div style="font-size:1.5em; text-align:center; margin-bottom:10px;">
                Level {current_level} - {total_points} Points
            </div>
            <div style="width:100%; background-color:#2C5282; border-radius:5px; height:30px; position:relative;">
                <div style="width:{percent_to_next*100}%; height:30px; background-color:#3B82F6; border-radius:5px;"></div>
                <div style="position:absolute; top:0; width:100%; height:30px; display:flex; align-items:center; justify-content:center;">
                    {progress_to_next_level}/{points_per_level} to Level {current_level+1}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ------ Main Application Sections ------

def display_dashboard(user_progress: UserProgress):
    """Display the student dashboard."""
    st.subheader("📊 Your Security Dashboard")
    
    # Level and progress
    render_level_progress(user_progress.current_level, user_progress.total_points)
    
    # Statistics row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Security Score", f"{user_progress.security_score:.1f}%")
    with col2:
        st.metric("Scenarios Completed", f"{len(user_progress.completed_scenarios)}/5")
    with col3:
        st.metric("Badges Earned", f"{len(user_progress.badges)}/10")
    
    # Badges section
    st.subheader("🏆 Your Badges")
    
    all_badges = get_sample_badges()
    
    badge_cols = st.columns(5)
    for i, badge in enumerate(all_badges):
        with badge_cols[i % 5]:
            render_badge(badge, badge['id'] in user_progress.badges)
    
    # Recent activity
    st.subheader("📝 Recent Activity")
    if not user_progress.completed_scenarios:
        st.info("You haven't completed any security scenarios yet. Start your first challenge below!")
    else:
        activity_data = []
        scenarios = get_sample_scenarios()
        scenario_dict = {s.id: s for s in scenarios}
        
        for scenario_id in user_progress.completed_scenarios:
            if scenario_id in scenario_dict:
                scenario = scenario_dict[scenario_id]
                activity_data.append({
                    "Scenario": scenario.title,
                    "Type": scenario.scenario_type.capitalize(),
                    "Difficulty": scenario.difficulty,
                    "Points": scenario.points,
                    "Date Completed": "Today"  # In a real app, would store actual timestamps
                })
        
        if activity_data:
            st.dataframe(pd.DataFrame(activity_data))


def display_scenario_browser():
    """Display the scenario browser for selecting challenges."""
    st.subheader("🎮 Security Challenge Library")
    
    # Get scenarios and user progress
    scenarios = get_sample_scenarios()
    user_progress = get_sample_user_progress()
    
    # Display scenarios in expandable cards with "Start" buttons
    for scenario in scenarios:
        completed = scenario.id in user_progress.completed_scenarios
        status = "✅ Completed" if completed else "🔸 Available"
        status_color = "#4CAF50" if completed else "#FFC107"
        
        with st.expander(f"{scenario.title} - {status}"):
            # Two columns: info and start button
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**Description:** {scenario.description}")
                st.markdown(f"**Difficulty:** {scenario.difficulty}")
                st.markdown(f"**Type:** {scenario.scenario_type.capitalize()}")
                st.markdown(f"**Points:** {scenario.points}")
            
            with col2:
                # Start button
                start_button = st.button("Start Challenge", key=f"start_{scenario.id}")
                if start_button:
                    st.session_state.active_scenario = scenario
                    st.rerun()


def display_scenario_simulator(scenario: SimulationScenario):
    """Display the active scenario simulation."""
    st.subheader(f"🎯 {scenario.title}")
    st.markdown(f"**{scenario.description}**")
    
    # Different rendering based on scenario type
    if scenario.scenario_type == "phishing":
        display_phishing_simulation(scenario)
    elif scenario.scenario_type == "password":
        display_password_simulation(scenario)
    elif scenario.scenario_type == "social_media":
        display_social_media_simulation(scenario)
    elif scenario.scenario_type == "network_security":
        display_network_security_simulation(scenario)
    elif scenario.scenario_type == "device_security":
        display_device_security_simulation(scenario)
    
    # Exit button (always visible)
    exit_button = st.button("Exit Simulation")
    if exit_button:
        if hasattr(st.session_state, 'active_scenario'):
            del st.session_state.active_scenario
        st.rerun()


def display_phishing_simulation(scenario: SimulationScenario):
    """Display phishing email simulation."""
    # Get email content
    email = scenario.content["email"]
    
    # Display email interface
    st.markdown(
        f"""
        <div style="border:1px solid #ddd; border-radius:5px; padding:15px; margin-bottom:20px; background-color:#f9f9f9;">
            <div style="border-bottom:1px solid #ddd; padding-bottom:10px; margin-bottom:10px;">
                <div><strong>From:</strong> {email['from']}</div>
                <div><strong>Subject:</strong> {email['subject']}</div>
            </div>
            <div style="white-space: pre-line;">{email['body']}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Initialize simulation state if not existing
    if 'phishing_simulation_state' not in st.session_state:
        st.session_state.phishing_simulation_state = {
            'current_question': 0,
            'answers': [],
            'score': 0,
            'max_score': len(scenario.content["questions"]),
            'completed': False
        }
    
    state = st.session_state.phishing_simulation_state
    questions = scenario.content["questions"]
    
    # Only show questions if not completed
    if not state['completed']:
        # Display current question
        if state['current_question'] < len(questions):
            question = questions[state['current_question']]
            st.write(f"**Question {state['current_question'] + 1}:** {question['question']}")
            
            # Different handling based on question type
            if question.get('type') == 'multi':
                # Multi-select question
                options = st.multiselect(
                    "Select all that apply:",
                    question['options']
                )
                submit = st.button("Submit Answer")
                
                if submit:
                    # Check if answers match correct answers
                    correct_set = set(question['correct_answers'])
                    user_set = set(options)
                    correct = correct_set == user_set
                    
                    # Store answer and update score
                    state['answers'].append({
                        'question': question['question'],
                        'user_answer': options,
                        'correct_answer': question['correct_answers'],
                        'is_correct': correct
                    })
                    
                    if correct:
                        state['score'] += 1
                    
                    # Move to next question
                    state['current_question'] += 1
                    st.rerun()
            else:
                # Single-select question
                option = st.radio(
                    "Select one:",
                    question['options']
                )
                submit = st.button("Submit Answer")
                
                if submit:
                    # Check if answer is correct
                    correct = option == question['correct_answer']
                    
                    # Store answer and update score
                    state['answers'].append({
                        'question': question['question'],
                        'user_answer': option,
                        'correct_answer': question['correct_answer'],
                        'is_correct': correct
                    })
                    
                    if correct:
                        state['score'] += 1
                    
                    # Move to next question
                    state['current_question'] += 1
                    st.rerun()
        else:
            # All questions answered, show results
            state['completed'] = True
            score_percent = (state['score'] / state['max_score']) * 100
            
            # Update user progress
            update_user_progress_after_scenario(scenario.id, score_percent, scenario.points)
            
            st.rerun()
    
    # Show results if completed
    if state['completed']:
        score_percent = (state['score'] / state['max_score']) * 100
        
        # Show overall score
        if score_percent >= 80:
            st.success(f"Great job! You scored {score_percent:.1f}%")
            st.balloons()
        elif score_percent >= 60:
            st.warning(f"Good attempt! You scored {score_percent:.1f}%")
        else:
            st.error(f"You need more practice. You scored {score_percent:.1f}%")
        
        # Display red flags
        st.subheader("Email Red Flags:")
        for flag in email['red_flags']:
            st.markdown(f"- {flag}")
        
        # Display question results
        st.subheader("Question Results:")
        for i, answer in enumerate(state['answers']):
            if answer['is_correct']:
                st.markdown(f"✅ **Question {i+1}:** {answer['question']}")
                st.markdown(f"Your answer: {answer['user_answer']} (Correct)")
            else:
                st.markdown(f"❌ **Question {i+1}:** {answer['question']}")
                st.markdown(f"Your answer: {answer['user_answer']}")
                st.markdown(f"Correct answer: {answer['correct_answer']}")
            st.markdown("---")
        
        # Reset button
        reset = st.button("Try Again")
        if reset:
            if 'phishing_simulation_state' in st.session_state:
                del st.session_state.phishing_simulation_state
            st.rerun()


def display_password_simulation(scenario: SimulationScenario):
    """Display password security simulation."""
    st.markdown(scenario.content["instruction"])
    
    # Initialize simulation state if not existing
    if 'password_simulation_state' not in st.session_state:
        st.session_state.password_simulation_state = {
            'created_password': '',
            'strength_score': 0,
            'password_feedback': [],
            'current_task': 0,
            'task_results': [],
            'current_question': 0,
            'answers': [],
            'score': 0,
            'max_score': len(scenario.content["questions"]),
            'completed': False
        }
    
    state = st.session_state.password_simulation_state
    
    # Task 1: Create password and check strength
    if state['current_task'] == 0:
        st.subheader("Task 1: Create a Strong Password")
        st.write(scenario.content["password_tasks"][0]["task"])
        
        # Password input
        password = st.text_input("Enter your password:", type="password")
        check_button = st.button("Check Strength")
        
        if check_button and password:
            # Evaluate password strength
            evaluation = scenario.content["password_tasks"][0]["evaluation"]
            strength_score = 0
            feedback = []
            
            # Length check
            if len(password) >= evaluation["min_length"]:
                strength_score += 25
                feedback.append("✅ Good length")
            else:
                feedback.append(f"❌ Password should be at least {evaluation['min_length']} characters")
            
            # Uppercase check
            if evaluation["require_uppercase"] and any(c.isupper() for c in password):
                strength_score += 25
                feedback.append("✅ Contains uppercase letters")
            elif evaluation["require_uppercase"]:
                feedback.append("❌ Missing uppercase letters")
            
            # Lowercase check
            if evaluation["require_lowercase"] and any(c.islower() for c in password):
                strength_score += 25
                feedback.append("✅ Contains lowercase letters")
            elif evaluation["require_lowercase"]:
                feedback.append("❌ Missing lowercase letters")
            
            # Number check
            if evaluation["require_numbers"] and any(c.isdigit() for c in password):
                strength_score += 25
                feedback.append("✅ Contains numbers")
            elif evaluation["require_numbers"]:
                feedback.append("❌ Missing numbers")
            
            # Special character check
            special_chars = "!@#$%^&*()_+-=[]{}|;:'\",.<>/?"
            if evaluation["require_special"] and any(c in special_chars for c in password):
                strength_score += 25
                feedback.append("✅ Contains special characters")
            elif evaluation["require_special"]:
                feedback.append("❌ Missing special characters")
            
            # Check for banned words
            for word in evaluation["banned_words"]:
                if word.lower() in password.lower():
                    strength_score = max(0, strength_score - 50)
                    feedback.append(f"❌ Contains common password '{word}'")
                    break
            
            # Update state
            state['created_password'] = password
            state['strength_score'] = strength_score
            state['password_feedback'] = feedback
            
            # Move to next task if password is strong enough
            if strength_score >= 100:
                state['current_task'] = 1
            
            st.rerun()
        
        # Display strength results if available
        if state['created_password']:
            # Show strength meter
            strength_color = "#4CAF50" if state['strength_score'] >= 100 else "#F44336"
            st.markdown(
                f"""
                <div style="margin-bottom:20px;">
                    <div style="font-weight:bold;">Password Strength: {state['strength_score']}%</div>
                    <div style="width:100%; background-color:#ddd; border-radius:5px;">
                        <div style="width:{state['strength_score']}%; height:20px; 
                             background-color:{strength_color}; border-radius:5px;"></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Show feedback
            for feedback_item in state['password_feedback']:
                st.markdown(feedback_item)
    
    # Task 2: Evaluate existing passwords
    elif state['current_task'] == 1:
        st.subheader("Task 2: Evaluate Existing Passwords")
        st.write(scenario.content["password_tasks"][1]["task"])
        
        # Show passwords to evaluate
        passwords = scenario.content["password_tasks"][1]["passwords"]
        
        for i, pwd in enumerate(passwords):
            secure_option = st.radio(
                f"Is this password secure? '{pwd['password']}'",
                ["Secure", "Not Secure"],
                key=f"pwd_{i}"
            )
            
            check_button = st.button("Check", key=f"check_pwd_{i}")
            
            if check_button:
                is_secure = secure_option == "Secure"
                correct = is_secure == pwd["is_secure"]
                
                # Add to results
                state['task_results'].append({
                    'password': pwd['password'],
                    'user_answer': is_secure,
                    'correct_answer': pwd["is_secure"],
                    'is_correct': correct
                })
                
                # Show next password or move to questions
                if len(state['task_results']) == len(passwords):
                    state['current_task'] = 2
                
                st.rerun()
    
    # Questions
    elif state['current_task'] == 2 and state['current_question'] < len(scenario.content["questions"]):
        st.subheader("Password Security Questions")
        
        question = scenario.content["questions"][state['current_question']]
        st.write(f"**Question {state['current_question'] + 1}:** {question['question']}")
        
        option = st.radio(
            "Select one:",
            question['options']
        )
        submit = st.button("Submit Answer")
        
        if submit:
            # Check if answer is correct
            correct = option == question['correct_answer']
            
            # Store answer and update score
            state['answers'].append({
                'question': question['question'],
                'user_answer': option,
                'correct_answer': question['correct_answer'],
                'is_correct': correct
            })
            
            if correct:
                state['score'] += 1
            
            # Move to next question
            state['current_question'] += 1
            
            # Mark as completed if all questions answered
            if state['current_question'] >= len(scenario.content["questions"]):
                state['completed'] = True
                score_percent = (state['score'] / state['max_score']) * 100
                update_user_progress_after_scenario(scenario.id, score_percent, scenario.points)
            
            st.rerun()
    
    # Show results if completed
    elif state['completed'] or state['current_task'] > 1 and state['current_question'] >= len(scenario.content["questions"]):
        st.subheader("Results")
        
        # Calculate overall score
        password_task_score = 100 if state['strength_score'] >= 100 else state['strength_score']
        evaluation_score = sum(1 for r in state['task_results'] if r['is_correct']) / len(state['task_results']) * 100
        question_score = (state['score'] / state['max_score']) * 100
        
        overall_score = (password_task_score + evaluation_score + question_score) / 3
        
        # Show overall score
        if overall_score >= 80:
            st.success(f"Great job! Your overall score: {overall_score:.1f}%")
            st.balloons()
        elif overall_score >= 60:
            st.warning(f"Good attempt! Your overall score: {overall_score:.1f}%")
        else:
            st.error(f"You need more practice. Your overall score: {overall_score:.1f}%")
        
        # Display question results
        st.subheader("Password Creation:")
        for feedback_item in state['password_feedback']:
            st.markdown(feedback_item)
        
        st.subheader("Password Evaluation Results:")
        for result in state['task_results']:
            if result['is_correct']:
                st.markdown(f"✅ Password: '{result['password']}' - Your answer: {'Secure' if result['user_answer'] else 'Not Secure'} (Correct)")
            else:
                st.markdown(f"❌ Password: '{result['password']}' - Your answer: {'Secure' if result['user_answer'] else 'Not Secure'}")
                st.markdown(f"Correct answer: {'Secure' if result['correct_answer'] else 'Not Secure'}")
        
        st.subheader("Question Results:")
        for i, answer in enumerate(state['answers']):
            if answer['is_correct']:
                st.markdown(f"✅ **Question {i+1}:** {answer['question']}")
                st.markdown(f"Your answer: {answer['user_answer']} (Correct)")
            else:
                st.markdown(f"❌ **Question {i+1}:** {answer['question']}")
                st.markdown(f"Your answer: {answer['user_answer']}")
                st.markdown(f"Correct answer: {answer['correct_answer']}")
        
        # Reset button
        reset = st.button("Try Again")
        if reset:
            if 'password_simulation_state' in st.session_state:
                del st.session_state.password_simulation_state
            st.rerun()


def display_social_media_simulation(scenario: SimulationScenario):
    """Display social media security simulation."""
    st.markdown(scenario.content["instruction"])
    
    # Initialize simulation state if not existing
    if 'social_media_simulation_state' not in st.session_state:
        st.session_state.social_media_simulation_state = {
            'current_stage': 'settings_review',
            'selected_settings': [],
            'current_question': 0,
            'answers': [],
            'score': 0,
            'max_score': len(scenario.content["questions"]) + 1,  # +1 for the settings task
            'completed': False
        }
    
    state = st.session_state.social_media_simulation_state
    
    # Stage 1: Review and fix settings
    if state['current_stage'] == 'settings_review':
        st.subheader("Social Media Privacy Settings")
        
        # Display current settings
        settings = scenario.content["account_setup"]["current_settings"]
        
        st.markdown("### Current Account Settings")
        settings_df = pd.DataFrame(settings)
        st.table(settings_df)
        
        # Action task - select settings to change
        st.markdown("### Action Required")
        action_task = scenario.content["action_tasks"][0]
        st.write(action_task["task"])
        
        selected_settings = st.multiselect(
            "Select settings to change:",
            action_task["options"]
        )
        
        apply_changes = st.button("Apply Changes")
        
        if apply_changes:
            # Check if correct settings were changed
            correct_set = set(action_task["correct_answers"])
            user_set = set(selected_settings)
            all_correct = correct_set == user_set
            
            # Update state
            state['selected_settings'] = selected_settings
            
            # Update score based on settings task
            if all_correct:
                state['score'] += 1
            
            # Move to questions
            state['current_stage'] = 'questions'
            st.rerun()
    
    # Stage 2: Questions
    elif state['current_stage'] == 'questions' and state['current_question'] < len(scenario.content["questions"]):
        st.subheader("Social Media Privacy Questions")
        
        question = scenario.content["questions"][state['current_question']]
        st.write(f"**Question {state['current_question'] + 1}:** {question['question']}")
        
        option = st.radio(
            "Select one:",
            question['options']
        )
        submit = st.button("Submit Answer")
        
        if submit:
            # Check if answer is correct
            correct = option == question['correct_answer']
            
            # Store answer and update score
            state['answers'].append({
                'question': question['question'],
                'user_answer': option,
                'correct_answer': question['correct_answer'],
                'is_correct': correct
            })
            
            if correct:
                state['score'] += 1
            
            # Move to next question
            state['current_question'] += 1
            
            # Mark as completed if all questions answered
            if state['current_question'] >= len(scenario.content["questions"]):
                state['completed'] = True
                score_percent = (state['score'] / state['max_score']) * 100
                update_user_progress_after_scenario(scenario.id, score_percent, scenario.points)
            
            st.rerun()
    
    # Show results if completed
    elif state['completed'] or (state['current_stage'] == 'questions' and state['current_question'] >= len(scenario.content["questions"])):
        # Mark as completed if not already
        if not state['completed']:
            state['completed'] = True
            score_percent = (state['score'] / state['max_score']) * 100
            update_user_progress_after_scenario(scenario.id, score_percent, scenario.points)
        
        st.subheader("Results")
        
        # Calculate score
        score_percent = (state['score'] / state['max_score']) * 100
        
        # Show overall score
        if score_percent >= 80:
            st.success(f"Great job! Your score: {score_percent:.1f}%")
            st.balloons()
        elif score_percent >= 60:
            st.warning(f"Good attempt! Your score: {score_percent:.1f}%")
        else:
            st.error(f"You need more practice. Your score: {score_percent:.1f}%")
        
        # Display settings results
        st.subheader("Privacy Settings Review:")
        
        action_task = scenario.content["action_tasks"][0]
        correct_set = set(action_task["correct_answers"])
        user_set = set(state['selected_settings'])
        
        if correct_set == user_set:
            st.markdown("✅ You correctly identified all settings that needed to be changed!")
        else:
            st.markdown("❌ You missed some settings that needed to be changed.")
            
            st.markdown("**You selected:**")
            for setting in state['selected_settings']:
                st.markdown(f"- {setting}")
            
            st.markdown("**Correct settings to change:**")
            for setting in action_task["correct_answers"]:
                st.markdown(f"- {setting}")
        
        # Display question results
        st.subheader("Question Results:")
        for i, answer in enumerate(state['answers']):
            if answer['is_correct']:
                st.markdown(f"✅ **Question {i+1}:** {answer['question']}")
                st.markdown(f"Your answer: {answer['user_answer']} (Correct)")
            else:
                st.markdown(f"❌ **Question {i+1}:** {answer['question']}")
                st.markdown(f"Your answer: {answer['user_answer']}")
                st.markdown(f"Correct answer: {answer['correct_answer']}")
        
        # Reset button
        reset = st.button("Try Again")
        if reset:
            if 'social_media_simulation_state' in st.session_state:
                del st.session_state.social_media_simulation_state
            st.rerun()


def display_network_security_simulation(scenario: SimulationScenario):
    """Display network security simulation."""
    st.markdown(f"### Scenario: {scenario.content['scenario']}")
    
    # Initialize simulation state if not existing
    if 'network_simulation_state' not in st.session_state:
        st.session_state.network_simulation_state = {
            'selected_action': None,
            'action_evaluated': False,
            'current_question': 0,
            'answers': [],
            'score': 0,
            'max_score': len(scenario.content["questions"]) + 1,  # +1 for the action selection
            'completed': False
        }
    
    state = st.session_state.network_simulation_state
    
    # Stage 1: Select action
    if not state['action_evaluated']:
        st.subheader("What would you do in this situation?")
        
        # Display options
        options = [action['action'] for action in scenario.content['options']]
        
        selected_action = st.radio(
            "Select your action:",
            options
        )
        
        # Find the selected action data
        selected_action_data = next((a for a in scenario.content['options'] if a['action'] == selected_action), None)
        
        take_action = st.button("Take Action")
        
        if take_action and selected_action_data:
            # Update state
            state['selected_action'] = selected_action_data
            state['action_evaluated'] = True
            
            # Update score based on action
            if selected_action_data['is_secure']:
                state['score'] += 1
            
            st.rerun()
    
    # Evaluate action if taken
    elif state['action_evaluated'] and state['current_question'] == 0:
        st.subheader("Action Result")
        
        action = state['selected_action']
        if action['is_secure']:
            st.success(f"Good choice! {action['explanation']}")
        else:
            st.error(f"This is risky! {action['explanation']}")
        
        # Continue to questions
        continue_button = st.button("Continue to Questions")
        if continue_button:
            # Move to questions
            state['current_question'] = 1
            st.rerun()
    
    # Stage 2: Questions
    elif state['current_question'] > 0 and state['current_question'] <= len(scenario.content["questions"]):
        st.subheader("Network Security Questions")
        
        question_index = state['current_question'] - 1
        question = scenario.content["questions"][question_index]
        
        st.write(f"**Question {state['current_question']}:** {question['question']}")
        
        option = st.radio(
            "Select one:",
            question['options']
        )
        submit = st.button("Submit Answer")
        
        if submit:
            # Check if answer is correct
            correct = option == question['correct_answer']
            
            # Store answer and update score
            state['answers'].append({
                'question': question['question'],
                'user_answer': option,
                'correct_answer': question['correct_answer'],
                'is_correct': correct
            })
            
            if correct:
                state['score'] += 1
            
            # Move to next question
            state['current_question'] += 1
            
            # Mark as completed if all questions answered
            if state['current_question'] > len(scenario.content["questions"]):
                state['completed'] = True
                score_percent = (state['score'] / state['max_score']) * 100
                update_user_progress_after_scenario(scenario.id, score_percent, scenario.points)
            
            st.rerun()
    
    # Show results if completed
    elif state['completed'] or (state['current_question'] > len(scenario.content["questions"])):
        # Mark as completed if not already
        if not state['completed']:
            state['completed'] = True
            score_percent = (state['score'] / state['max_score']) * 100
            update_user_progress_after_scenario(scenario.id, score_percent, scenario.points)
        
        st.subheader("Results")
        
        # Calculate score
        score_percent = (state['score'] / state['max_score']) * 100
        
        # Show overall score
        if score_percent >= 80:
            st.success(f"Great job! Your score: {score_percent:.1f}%")
            st.balloons()
        elif score_percent >= 60:
            st.warning(f"Good attempt! Your score: {score_percent:.1f}%")
        else:
            st.error(f"You need more practice. Your score: {score_percent:.1f}%")
        
        # Display action result
        st.subheader("Your Action:")
        action = state['selected_action']
        if action['is_secure']:
            st.markdown(f"✅ **{action['action']}**")
            st.markdown(f"This was a secure choice. {action['explanation']}")
        else:
            st.markdown(f"❌ **{action['action']}**")
            st.markdown(f"This was a risky choice. {action['explanation']}")
        
        # Display secure options
        st.markdown("**Secure options were:**")
        for option in scenario.content['options']:
            if option['is_secure']:
                st.markdown(f"- {option['action']} - {option['explanation']}")
        
        # Display question results
        st.subheader("Question Results:")
        for i, answer in enumerate(state['answers']):
            if answer['is_correct']:
                st.markdown(f"✅ **Question {i+1}:** {answer['question']}")
                st.markdown(f"Your answer: {answer['user_answer']} (Correct)")
            else:
                st.markdown(f"❌ **Question {i+1}:** {answer['question']}")
                st.markdown(f"Your answer: {answer['user_answer']}")
                st.markdown(f"Correct answer: {answer['correct_answer']}")
        
        # Reset button
        reset = st.button("Try Again")
        if reset:
            if 'network_simulation_state' in st.session_state:
                del st.session_state.network_simulation_state
            st.rerun()


def display_device_security_simulation(scenario: SimulationScenario):
    """Display device security simulation."""
    st.markdown(scenario.content["instruction"])
    
    # Initialize simulation state if not existing
    if 'device_simulation_state' not in st.session_state:
        st.session_state.device_simulation_state = {
            'current_stage': 'device_audit',
            'selected_settings': [],
            'current_question': 0,
            'answers': [],
            'score': 0,
            'max_score': len(scenario.content["questions"]) + 1,  # +1 for the settings task
            'completed': False
        }
    
    state = st.session_state.device_simulation_state
    
    # Stage 1: Audit device settings
    if state['current_stage'] == 'device_audit':
        st.subheader("Device Security Audit")
        
        # Display current settings
        settings = scenario.content["device_status"]
        
        settings_table = []
        for setting in settings:
            settings_table.append({
                "Setting": setting["setting"],
                "Current Status": setting["current"],
                "Recommended": setting["recommended"]
            })
        
        st.table(pd.DataFrame(settings_table))
        
        # Action task - select settings to fix
        st.markdown("### Action Required")
        action_task = scenario.content["action_tasks"][0]
        st.write(action_task["task"])
        
        selected_settings = st.multiselect(
            "Select settings to fix:",
            action_task["options"]
        )
        
        apply_changes = st.button("Apply Changes")
        
        if apply_changes:
            # Check if correct settings were selected
            correct_set = set(action_task["correct_answers"])
            user_set = set(selected_settings)
            all_correct = correct_set == user_set
            
            # Update state
            state['selected_settings'] = selected_settings
            
            # Update score based on settings task
            if all_correct:
                state['score'] += 1
            
            # Move to questions
            state['current_stage'] = 'questions'
            st.rerun()
    
    # Stage 2: Questions
    elif state['current_stage'] == 'questions' and state['current_question'] < len(scenario.content["questions"]):
        st.subheader("Device Security Questions")
        
        question = scenario.content["questions"][state['current_question']]
        st.write(f"**Question {state['current_question'] + 1}:** {question['question']}")
        
        option = st.radio(
            "Select one:",
            question['options']
        )
        submit = st.button("Submit Answer")
        
        if submit:
            # Check if answer is correct
            correct = option == question['correct_answer']
            
            # Store answer and update score
            state['answers'].append({
                'question': question['question'],
                'user_answer': option,
                'correct_answer': question['correct_answer'],
                'is_correct': correct
            })
            
            if correct:
                state['score'] += 1
            
            # Move to next question
            state['current_question'] += 1
            
            # Mark as completed if all questions answered
            if state['current_question'] >= len(scenario.content["questions"]):
                state['completed'] = True
                score_percent = (state['score'] / state['max_score']) * 100
                update_user_progress_after_scenario(scenario.id, score_percent, scenario.points)
            
            st.rerun()
    
    # Show results if completed
    elif state['completed'] or (state['current_stage'] == 'questions' and state['current_question'] >= len(scenario.content["questions"])):
        # Mark as completed if not already
        if not state['completed']:
            state['completed'] = True
            score_percent = (state['score'] / state['max_score']) * 100
            update_user_progress_after_scenario(scenario.id, score_percent, scenario.points)
        
        st.subheader("Results")
        
        # Calculate score
        score_percent = (state['score'] / state['max_score']) * 100
        
        # Show overall score
        if score_percent >= 80:
            st.success(f"Great job! Your score: {score_percent:.1f}%")
            st.balloons()
        elif score_percent >= 60:
            st.warning(f"Good attempt! Your score: {score_percent:.1f}%")
        else:
            st.error(f"You need more practice. Your score: {score_percent:.1f}%")
        
        # Display settings results
        st.subheader("Device Security Audit Results:")
        
        action_task = scenario.content["action_tasks"][0]
        correct_set = set(action_task["correct_answers"])
        user_set = set(state['selected_settings'])
        
        if correct_set == user_set:
            st.markdown("✅ You correctly identified all settings that needed to be fixed!")
        else:
            st.markdown("❌ You missed some settings that needed to be fixed.")
            
            st.markdown("**You selected:**")
            for setting in state['selected_settings']:
                st.markdown(f"- {setting}")
            
            st.markdown("**All settings that needed to be fixed:**")
            for setting in action_task["correct_answers"]:
                st.markdown(f"- {setting}")
        
        # Display question results
        st.subheader("Question Results:")
        for i, answer in enumerate(state['answers']):
            if answer['is_correct']:
                st.markdown(f"✅ **Question {i+1}:** {answer['question']}")
                st.markdown(f"Your answer: {answer['user_answer']} (Correct)")
            else:
                st.markdown(f"❌ **Question {i+1}:** {answer['question']}")
                st.markdown(f"Your answer: {answer['user_answer']}")
                st.markdown(f"Correct answer: {answer['correct_answer']}")
        
        # Reset button
        reset = st.button("Try Again")
        if reset:
            if 'device_simulation_state' in st.session_state:
                del st.session_state.device_simulation_state
            st.rerun()


def display_teacher_dashboard():
    """Display the teacher dashboard."""
    st.subheader("👨‍🏫 Teacher Dashboard")
    
    st.write("""
    This dashboard helps teachers track student progress through the cybersecurity
    curriculum and identify areas where students may need additional support.
    """)
    
    # Get sample class data
    class_data = get_sample_class_data()
    
    # Class overview tab and detailed student data tab
    tab1, tab2, tab3 = st.tabs(["Class Overview", "Student Details", "Risk Analysis"])
    
    with tab1:
        st.subheader("Class Performance")
        
        # Summary metrics
        avg_score = sum(student["security_score"] for student in class_data) / len(class_data)
        completed_scenarios = sum(student["completed_scenarios"] for student in class_data)
        high_risk_behaviors = sum(student["high_risk_behaviors"] for student in class_data)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Average Security Score", f"{avg_score:.1f}%")
        with col2:
            st.metric("Total Completed Scenarios", completed_scenarios)
        with col3:
            st.metric("Total High-Risk Behaviors", high_risk_behaviors)
        
        # Security score distribution
        st.subheader("Security Score Distribution")
        
        df_class = pd.DataFrame(class_data)
        
        fig = px.histogram(
            df_class,
            x="security_score",
            nbins=10,
            title="Distribution of Security Scores",
            labels={"security_score": "Security Score", "count": "Number of Students"},
            color_discrete_sequence=["#3B82F6"]
        )
        
        fig.update_layout(
            xaxis_title="Security Score (%)",
            yaxis_title="Number of Students"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Progress chart
        st.subheader("Scenario Completion Progress")
        
        # Create progress bars for each student
        progress_data = []
        for student in class_data:
            progress = (student["completed_scenarios"] / 10) * 100  # Assuming 10 total scenarios
            progress_data.append({
                "Student": student["name"],
                "Progress (%)": progress
            })
        
        progress_df = pd.DataFrame(progress_data)
        progress_df = progress_df.sort_values(by="Progress (%)", ascending=False)
        
        fig = px.bar(
            progress_df,
            y="Student",
            x="Progress (%)",
            orientation="h",
            title="Scenario Completion by Student",
            color="Progress (%)",
            color_continuous_scale=px.colors.sequential.Viridis
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Student Performance Details")
        
        # Student data table
        st.dataframe(pd.DataFrame(class_data))
        
        # Select a student for detailed view
        student_names = [student["name"] for student in class_data]
        selected_student = st.selectbox("Select a student for detailed view:", student_names)
        
        # Get selected student data
        student_data = next((s for s in class_data if s["name"] == selected_student), None)
        
        if student_data:
            st.subheader(f"Detailed View: {student_data['name']}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Security Score", f"{student_data['security_score']}%")
                st.metric("Completed Scenarios", f"{student_data['completed_scenarios']}/10")
            with col2:
                st.metric("Grade", student_data["grade"])
                st.metric("High-Risk Behaviors", student_data["high_risk_behaviors"])
            
            # Create a circular gauge chart for security score
            fig = px.pie(
                values=[student_data['security_score'], 100 - student_data['security_score']],
                names=["Score", "Remaining"],
                hole=0.7,
                color_discrete_sequence=["#4CAF50", "#EEEEEE"]
            )
            
            fig.update_layout(
                annotations=[dict(text=f"{student_data['security_score']}%", x=0.5, y=0.5, font_size=20, showarrow=False)],
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Recommendations
            st.subheader("Recommendations")
            
            if student_data["security_score"] < 75:
                st.warning("This student needs additional support with cybersecurity concepts.")
                st.markdown("Recommended actions:")
                st.markdown("1. Schedule a one-on-one session to review security fundamentals")
                st.markdown("2. Assign remedial scenarios focused on identified weak areas")
                st.markdown("3. Provide simplified reference materials for key concepts")
            elif student_data["high_risk_behaviors"] > 2:
                st.warning("This student has demonstrated multiple high-risk behaviors.")
                st.markdown("Recommended actions:")
                st.markdown("1. Review specific high-risk behaviors identified in simulations")
                st.markdown("2. Assign focused scenarios that address these behaviors")
                st.markdown("3. Schedule a follow-up assessment in 2 weeks")
            else:
                st.success("This student is performing well in cybersecurity concepts.")
                st.markdown("Recommended actions:")
                st.markdown("1. Provide advanced scenarios to further challenge their skills")
                st.markdown("2. Consider having them mentor peers who are struggling")
                st.markdown("3. Introduce more complex cybersecurity topics")
    
    with tab3:
        st.subheader("Risk Analysis")
        
        # Create risk matrix
        risk_data = []
        for student in class_data:
            # Calculate risk level (higher score = lower risk)
            risk_score = 100 - student["security_score"] + (student["high_risk_behaviors"] * 5)
            
            risk_level = "Low"
            if risk_score > 30:
                risk_level = "Medium"
            if risk_score > 50:
                risk_level = "High"
            
            risk_data.append({
                "Student": student["name"],
                "Risk Score": risk_score,
                "Risk Level": risk_level,
                "Security Score": student["security_score"],
                "High-Risk Behaviors": student["high_risk_behaviors"]
            })
        
        risk_df = pd.DataFrame(risk_data)
        
        # Risk distribution chart
        fig = px.scatter(
            risk_df,
            x="Security Score",
            y="High-Risk Behaviors",
            color="Risk Level",
            size="Risk Score",
            hover_name="Student",
            title="Student Risk Matrix",
            color_discrete_map={
                "Low": "#4CAF50",
                "Medium": "#FFC107",
                "High": "#F44336"
            }
        )
        
        fig.update_layout(
            xaxis=dict(title="Security Score (%)", autorange="reversed"),
            yaxis=dict(title="High-Risk Behaviors")
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Risk level breakdown
        risk_counts = risk_df["Risk Level"].value_counts().reset_index()
        risk_counts.columns = ["Risk Level", "Count"]
        
        fig = px.pie(
            risk_counts,
            values="Count",
            names="Risk Level",
            title="Risk Level Distribution",
            color="Risk Level",
            color_discrete_map={
                "Low": "#4CAF50",
                "Medium": "#FFC107",
                "High": "#F44336"
            }
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # High risk student list
        high_risk_students = risk_df[risk_df["Risk Level"] == "High"]
        if not high_risk_students.empty:
            st.subheader("High Risk Students")
            st.dataframe(high_risk_students[["Student", "Risk Score", "Security Score", "High-Risk Behaviors"]])
            
            st.warning("""
            **Recommended Actions for High Risk Students:**
            1. Schedule immediate one-on-one intervention sessions
            2. Provide targeted remedial scenarios
            3. Implement more frequent progress checks
            4. Consider parent/guardian communication
            """)
        else:
            st.success("No students are currently in the high-risk category.")


# ------ Helper Functions ------

def update_user_progress_after_scenario(scenario_id: int, score_percent: float, points: int):
    """Update user progress after completing a scenario."""
    user_progress = get_sample_user_progress()
    
    # Add scenario to completed list if not already there
    if scenario_id not in user_progress.completed_scenarios:
        user_progress.completed_scenarios.append(scenario_id)
    
    # Add points based on score percentage (partial or full)
    earned_points = int(points * (score_percent / 100))
    user_progress.total_points += earned_points
    
    # Calculate level based on points
    points_per_level = 500
    user_progress.current_level = max(1, (user_progress.total_points // points_per_level) + 1)
    
    # Update security score (average of all scenario scores)
    # In a real app, would store individual scenario scores and calculate average
    user_progress.security_score = score_percent
    
    # Add badges based on achievements
    scenarios = get_sample_scenarios()
    all_badges = get_sample_badges()
    
    # Check for scenario-specific badges
    completed_types = [s.scenario_type for s in scenarios if s.id in user_progress.completed_scenarios]
    
    # Add phishing expert badge
    if "phishing" in completed_types and "phishing_expert" not in user_progress.badges:
        user_progress.badges.append("phishing_expert")
    
    # Add password master badge
    if "password" in completed_types and "password_master" not in user_progress.badges:
        user_progress.badges.append("password_master")
    
    # Add social guardian badge
    if "social_media" in completed_types and "social_guardian" not in user_progress.badges:
        user_progress.badges.append("social_guardian")
    
    # Add wifi warrior badge
    if "network_security" in completed_types and "wifi_warrior" not in user_progress.badges:
        user_progress.badges.append("wifi_warrior")
    
    # Add device defender badge
    if "device_security" in completed_types and "device_defender" not in user_progress.badges:
        user_progress.badges.append("device_defender")
    
    # Add level badges based on number of completed scenarios
    num_completed = len(user_progress.completed_scenarios)
    
    if num_completed >= 1 and "security_novice" not in user_progress.badges:
        user_progress.badges.append("security_novice")
    
    if num_completed >= 2 and "security_apprentice" not in user_progress.badges:
        user_progress.badges.append("security_apprentice")
    
    if num_completed >= 3 and "security_adept" not in user_progress.badges:
        user_progress.badges.append("security_adept")
    
    if num_completed >= 4 and "security_expert" not in user_progress.badges:
        user_progress.badges.append("security_expert")
    
    # Add perfect score badge
    if score_percent >= 100 and "perfect_score" not in user_progress.badges:
        user_progress.badges.append("perfect_score")
    
    # Update session state
    st.session_state.cybersafe_user_progress = user_progress


# ------ Main Application Function ------

def run_cybersafe_campus():
    """Main entry point for the CyberSafe Campus application."""
    run_cybersafe_header()
    
    # Sidebar with navigation
    st.sidebar.title("CyberSafe Navigation")
    
    # Role selection
    role = st.sidebar.radio(
        "Select your role:",
        ["Student", "Teacher"]
    )
    
    # Different navigation based on role
    if role == "Student":
        page = st.sidebar.radio(
            "Navigate to:",
            ["Dashboard", "Security Challenges"]
        )
        
        if page == "Dashboard":
            # Display student dashboard
            display_dashboard(get_sample_user_progress())
            
        elif page == "Security Challenges":
            # Check if there's an active scenario
            if hasattr(st.session_state, 'active_scenario'):
                # Display the active scenario
                display_scenario_simulator(st.session_state.active_scenario)
            else:
                # Display list of scenarios to choose from
                display_scenario_browser()
    
    elif role == "Teacher":
        # Teacher view is simpler - just the dashboard
        display_teacher_dashboard()


if __name__ == "__main__":
    run_cybersafe_campus()