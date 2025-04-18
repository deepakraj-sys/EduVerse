"""
This module provides interactive learning features for the EduVerse platform.
"""

# Define learning content structured by module
learning_content = {
    # K-12 Foundational Learning
    "Playtory": {
        "lessons": [
            {
                "title": "The Math Adventure",
                "description": "Learn basic arithmetic through an interactive story about space explorers.",
                "content_type": "story",
                "difficulty": "Beginner",
                "duration_minutes": 20,
                "skills": ["Addition", "Subtraction", "Problem Solving"]
            },
            {
                "title": "Science of Colors",
                "description": "Discover the science of light and colors through an interactive narrative.",
                "content_type": "story",
                "difficulty": "Intermediate",
                "duration_minutes": 25,
                "skills": ["Light Physics", "Color Theory", "Observation"]
            }
        ],
        "quizzes": [
            {
                "title": "Math Adventure Quiz",
                "questions": [
                    {
                        "question": "If the space explorers collected 7 moon rocks and then found 5 more, how many rocks do they have in total?",
                        "options": ["10", "11", "12", "13"],
                        "answer": "12"
                    },
                    {
                        "question": "The explorers shared 8 food packets equally among 4 crew members. How many packets did each person get?",
                        "options": ["1", "2", "3", "4"],
                        "answer": "2"
                    }
                ]
            }
        ]
    },
    
    "MathQuest Land": {
        "lessons": [
            {
                "title": "Fraction Kingdom",
                "description": "Explore the Fraction Kingdom and learn how to add, subtract, and compare fractions.",
                "content_type": "game",
                "difficulty": "Intermediate",
                "duration_minutes": 30,
                "skills": ["Fractions", "Comparison", "Addition", "Subtraction"]
            },
            {
                "title": "Multiplication Mountain",
                "description": "Climb Multiplication Mountain by solving increasingly difficult multiplication problems.",
                "content_type": "game",
                "difficulty": "Intermediate",
                "duration_minutes": 25,
                "skills": ["Multiplication", "Pattern Recognition", "Mental Math"]
            }
        ],
        "quizzes": [
            {
                "title": "Fraction Kingdom Quiz",
                "questions": [
                    {
                        "question": "Which fraction is larger: 3/4 or 2/3?",
                        "options": ["3/4", "2/3", "They are equal", "Cannot be determined"],
                        "answer": "3/4"
                    },
                    {
                        "question": "What is 1/2 + 1/4?",
                        "options": ["1/6", "2/6", "3/4", "1"],
                        "answer": "3/4"
                    }
                ]
            }
        ]
    },
    
    # Cybersecurity Education
    "CyberSafe Campus": {
        "lessons": [
            {
                "title": "Phishing Detection 101",
                "description": "Learn to identify phishing attempts and protect your information.",
                "content_type": "simulation",
                "difficulty": "Beginner",
                "duration_minutes": 35,
                "skills": ["Email Security", "Phishing Detection", "Digital Literacy"]
            },
            {
                "title": "Password Fortresses",
                "description": "Create strong, secure passwords and understand authentication methods.",
                "content_type": "interactive",
                "difficulty": "Beginner",
                "duration_minutes": 20,
                "skills": ["Password Security", "Authentication", "Personal Security"]
            }
        ],
        "quizzes": [
            {
                "title": "Phishing Detection Quiz",
                "questions": [
                    {
                        "question": "Which of the following is a common indicator of a phishing email?",
                        "options": [
                            "Email comes from someone you know",
                            "Urgent call to action",
                            "Professional formatting",
                            "Specific greeting with your name"
                        ],
                        "answer": "Urgent call to action"
                    },
                    {
                        "question": "What should you do if you receive a suspicious email asking for personal information?",
                        "options": [
                            "Reply asking for verification",
                            "Click links to investigate",
                            "Forward to IT security or delete",
                            "Provide minimal information only"
                        ],
                        "answer": "Forward to IT security or delete"
                    }
                ]
            }
        ]
    },
    
    # Engineering Disciplines
    "BodyVerse Blueprint": {
        "lessons": [
            {
                "title": "Circulatory System Simulation",
                "description": "Build and test a working model of the human circulatory system.",
                "content_type": "simulation",
                "difficulty": "Advanced",
                "duration_minutes": 45,
                "skills": ["Human Anatomy", "Systems Thinking", "Biomedical Engineering"]
            },
            {
                "title": "Neurological Pathways",
                "description": "Map neural connections and understand brain function through interactive modeling.",
                "content_type": "simulation",
                "difficulty": "Advanced",
                "duration_minutes": 50,
                "skills": ["Neuroscience", "Neural Networks", "Brain Anatomy"]
            }
        ],
        "quizzes": [
            {
                "title": "Circulatory System Quiz",
                "questions": [
                    {
                        "question": "What is the function of red blood cells?",
                        "options": [
                            "Fighting infections",
                            "Carrying oxygen",
                            "Forming blood clots",
                            "Producing antibodies"
                        ],
                        "answer": "Carrying oxygen"
                    },
                    {
                        "question": "Which chamber of the heart pumps blood to the lungs?",
                        "options": [
                            "Left ventricle",
                            "Right ventricle",
                            "Left atrium",
                            "Right atrium"
                        ],
                        "answer": "Right ventricle"
                    }
                ]
            }
        ]
    }
}

# Define learning paths (structured sequences of content)
learning_paths = [
    {
        "name": "Intro to Mathematics",
        "description": "A foundational path for building math skills through gamified learning.",
        "modules": ["MathQuest Land", "Playtory"],
        "target_age": "6-10 years",
        "estimated_duration_hours": 8,
        "difficulty": "Beginner"
    },
    {
        "name": "Digital Citizenship & Safety",
        "description": "Essential knowledge for safe and responsible digital behavior.",
        "modules": ["CyberSafe Campus"],
        "target_age": "10+ years",
        "estimated_duration_hours": 6,
        "difficulty": "Beginner"
    },
    {
        "name": "Human Body Systems",
        "description": "Explore human biology through interactive simulations and models.",
        "modules": ["BodyVerse Blueprint"],
        "target_age": "14+ years",
        "estimated_duration_hours": 12,
        "difficulty": "Advanced"
    }
]

# Define progress tracking sample data
sample_progress = {
    "Playtory": {
        "lessons_completed": 1,
        "total_lessons": 2,
        "quizzes_completed": 0,
        "total_quizzes": 1,
        "avg_quiz_score": 0
    },
    "MathQuest Land": {
        "lessons_completed": 2,
        "total_lessons": 2,
        "quizzes_completed": 1,
        "total_quizzes": 1,
        "avg_quiz_score": 75
    },
    "CyberSafe Campus": {
        "lessons_completed": 1,
        "total_lessons": 2,
        "quizzes_completed": 1,
        "total_quizzes": 1,
        "avg_quiz_score": 90
    },
    "BodyVerse Blueprint": {
        "lessons_completed": 0,
        "total_lessons": 2,
        "quizzes_completed": 0,
        "total_quizzes": 1,
        "avg_quiz_score": 0
    }
}

# Helper functions
def get_all_learning_modules():
    """Returns a list of all module names that have learning content."""
    return list(learning_content.keys())

def get_module_learning_content(module_name):
    """Returns the learning content for a specific module."""
    return learning_content.get(module_name, None)

def get_all_learning_paths():
    """Returns all available learning paths."""
    return learning_paths

def get_learning_path_by_name(path_name):
    """Returns a specific learning path by name."""
    for path in learning_paths:
        if path["name"] == path_name:
            return path
    return None

def get_progress_for_module(module_name):
    """Returns the progress data for a specific module."""
    return sample_progress.get(module_name, None)

def get_quiz_for_module(module_name, quiz_title):
    """Returns a specific quiz for a module."""
    module = get_module_learning_content(module_name)
    if not module or "quizzes" not in module:
        return None
    
    for quiz in module["quizzes"]:
        if quiz["title"] == quiz_title:
            return quiz
    
    return None

def calculate_overall_progress():
    """Calculates overall learning progress across all modules."""
    total_lessons = 0
    completed_lessons = 0
    total_quizzes = 0
    completed_quizzes = 0
    quiz_scores = []
    
    for module, progress in sample_progress.items():
        total_lessons += progress["total_lessons"]
        completed_lessons += progress["lessons_completed"]
        total_quizzes += progress["total_quizzes"]
        completed_quizzes += progress["quizzes_completed"]
        
        if progress["avg_quiz_score"] > 0:
            quiz_scores.append(progress["avg_quiz_score"])
    
    avg_score = sum(quiz_scores) / len(quiz_scores) if quiz_scores else 0
    
    return {
        "lessons_progress": (completed_lessons / total_lessons) * 100 if total_lessons > 0 else 0,
        "quizzes_progress": (completed_quizzes / total_quizzes) * 100 if total_quizzes > 0 else 0,
        "avg_quiz_score": avg_score
    }

def get_content_type_distribution():
    """Returns distribution of content types across all modules."""
    content_types = {}
    
    for module_name, content in learning_content.items():
        for lesson in content.get("lessons", []):
            content_type = lesson["content_type"]
            if content_type in content_types:
                content_types[content_type] += 1
            else:
                content_types[content_type] = 1
    
    return {
        "types": list(content_types.keys()),
        "counts": list(content_types.values())
    }

def get_difficulty_distribution():
    """Returns distribution of difficulty levels across all modules."""
    difficulties = {}
    
    for module_name, content in learning_content.items():
        for lesson in content.get("lessons", []):
            difficulty = lesson["difficulty"]
            if difficulty in difficulties:
                difficulties[difficulty] += 1
            else:
                difficulties[difficulty] = 1
    
    return {
        "levels": list(difficulties.keys()),
        "counts": list(difficulties.values())
    }