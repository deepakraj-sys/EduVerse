"""
Database service for EduVerse application.
"""
import json
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
import database_models as models
from modules_data import all_modules
from api_integrations import api_integrations
from learning_features import (learning_content, learning_paths)

def create_user(db: Session, username: str, email: str, hashed_password: str, full_name: str = None, age: int = None):
    """
    Create a new user in the database.
    
    Args:
        db: Database session
        username: Username for the new user
        email: Email address for the new user
        hashed_password: Hashed password for security
        full_name: Optional full name
        age: Optional age
        
    Returns:
        The created user object
    """
    user = models.User(
        username=username,
        email=email,
        hashed_password=hashed_password,
        full_name=full_name,
        age=age
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_username(db: Session, username: str):
    """Get a user by username."""
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    """Get a user by email."""
    return db.query(models.User).filter(models.User.email == email).first()

def create_category(db: Session, name: str, description: str = None):
    """Create a new category."""
    category = models.Category(name=name, description=description)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

def get_category_by_name(db: Session, name: str):
    """Get a category by name."""
    return db.query(models.Category).filter(models.Category.name == name).first()

def create_module(db: Session, name: str, description: str, category_id: int, age_range: str, features=None):
    """Create a new educational module."""
    module = models.Module(
        name=name,
        description=description,
        category_id=category_id,
        age_range=age_range,
        features=features
    )
    db.add(module)
    db.commit()
    db.refresh(module)
    return module

def get_module_by_name(db: Session, name: str):
    """Get a module by name."""
    return db.query(models.Module).filter(models.Module.name == name).first()

def get_modules_by_category(db: Session, category_id: int):
    """Get all modules in a category."""
    return db.query(models.Module).filter(models.Module.category_id == category_id).all()

def create_lesson(db: Session, title: str, description: str, module_id: int, content_type: str,
                 difficulty: str, duration_minutes: int, skills=None, content=None):
    """Create a new lesson."""
    lesson = models.Lesson(
        title=title,
        description=description,
        module_id=module_id,
        content_type=content_type,
        difficulty=difficulty,
        duration_minutes=duration_minutes,
        skills=skills,
        content=content
    )
    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    return lesson

def get_lessons_by_module(db: Session, module_id: int):
    """Get all lessons for a module."""
    return db.query(models.Lesson).filter(models.Lesson.module_id == module_id).all()

def create_quiz(db: Session, title: str, module_id: int, questions, description: str = None):
    """Create a new quiz."""
    quiz = models.Quiz(
        title=title,
        module_id=module_id,
        questions=questions,
        description=description
    )
    db.add(quiz)
    db.commit()
    db.refresh(quiz)
    return quiz

def get_quizzes_by_module(db: Session, module_id: int):
    """Get all quizzes for a module."""
    return db.query(models.Quiz).filter(models.Quiz.module_id == module_id).all()

def create_learning_path(db: Session, name: str, description: str, target_age: str,
                        difficulty: str, estimated_duration_hours: int, modules):
    """Create a new learning path."""
    path = models.LearningPath(
        name=name,
        description=description,
        target_age=target_age,
        difficulty=difficulty,
        estimated_duration_hours=estimated_duration_hours,
        modules=modules
    )
    db.add(path)
    db.commit()
    db.refresh(path)
    return path

def get_learning_path_by_name(db: Session, name: str):
    """Get a learning path by name."""
    return db.query(models.LearningPath).filter(models.LearningPath.name == name).first()

def get_all_learning_paths(db: Session):
    """Get all learning paths."""
    return db.query(models.LearningPath).all()

def record_lesson_progress(db: Session, user_id: int, lesson_id: int, completed: bool = False,
                         time_spent_minutes: int = 0, last_position=None):
    """Record a user's progress on a lesson."""
    # Check if progress record already exists
    progress = db.query(models.LessonProgress).filter(
        models.LessonProgress.user_id == user_id,
        models.LessonProgress.lesson_id == lesson_id
    ).first()
    
    if progress:
        # Update existing record
        progress.completed = completed
        progress.time_spent_minutes += time_spent_minutes
        if completed and not progress.completion_date:
            progress.completion_date = datetime.utcnow()
        if last_position:
            progress.last_position = last_position
    else:
        # Create new record
        completion_date = datetime.utcnow() if completed else None
        progress = models.LessonProgress(
            user_id=user_id,
            lesson_id=lesson_id,
            completed=completed,
            completion_date=completion_date,
            time_spent_minutes=time_spent_minutes,
            last_position=last_position
        )
        db.add(progress)
    
    db.commit()
    db.refresh(progress)
    return progress

def record_quiz_result(db: Session, user_id: int, quiz_id: int, score: float, answers=None):
    """Record the result of a quiz attempt."""
    result = models.QuizResult(
        user_id=user_id,
        quiz_id=quiz_id,
        score=score,
        answers=answers
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return result

def get_user_quiz_results(db: Session, user_id: int):
    """Get all quiz results for a user."""
    return db.query(models.QuizResult).filter(models.QuizResult.user_id == user_id).all()

def enroll_in_learning_path(db: Session, user_id: int, learning_path_id: int):
    """Enroll a user in a learning path."""
    # Check if enrollment already exists
    enrollment = db.query(models.LearningPathEnrollment).filter(
        models.LearningPathEnrollment.user_id == user_id,
        models.LearningPathEnrollment.learning_path_id == learning_path_id
    ).first()
    
    if not enrollment:
        enrollment = models.LearningPathEnrollment(
            user_id=user_id,
            learning_path_id=learning_path_id
        )
        db.add(enrollment)
        db.commit()
        db.refresh(enrollment)
    
    return enrollment

def update_learning_path_progress(db: Session, user_id: int, learning_path_id: int, progress_percentage: float):
    """Update a user's progress in a learning path."""
    enrollment = db.query(models.LearningPathEnrollment).filter(
        models.LearningPathEnrollment.user_id == user_id,
        models.LearningPathEnrollment.learning_path_id == learning_path_id
    ).first()
    
    if enrollment:
        enrollment.progress_percentage = progress_percentage
        if progress_percentage >= 100.0 and not enrollment.completed:
            enrollment.completed = True
            enrollment.completion_date = datetime.utcnow()
        
        db.commit()
        db.refresh(enrollment)
    
    return enrollment

def get_user_learning_paths(db: Session, user_id: int):
    """Get all learning paths a user is enrolled in."""
    return db.query(models.LearningPathEnrollment).filter(
        models.LearningPathEnrollment.user_id == user_id
    ).all()

def calculate_user_stats(db: Session, user_id: int):
    """Calculate learning statistics for a user."""
    # Get completed lessons count
    lessons_completed = db.query(func.count(models.LessonProgress.id)).filter(
        models.LessonProgress.user_id == user_id,
        models.LessonProgress.completed == True
    ).scalar()
    
    # Get total time spent
    total_time = db.query(func.sum(models.LessonProgress.time_spent_minutes)).filter(
        models.LessonProgress.user_id == user_id
    ).scalar() or 0
    
    # Get average quiz score
    avg_score = db.query(func.avg(models.QuizResult.score)).filter(
        models.QuizResult.user_id == user_id
    ).scalar() or 0
    
    # Get completed learning paths
    paths_completed = db.query(func.count(models.LearningPathEnrollment.id)).filter(
        models.LearningPathEnrollment.user_id == user_id,
        models.LearningPathEnrollment.completed == True
    ).scalar()
    
    return {
        "lessons_completed": lessons_completed,
        "total_time_minutes": total_time,
        "average_quiz_score": avg_score,
        "learning_paths_completed": paths_completed
    }

def populate_sample_data(db: Session):
    """
    Populate the database with sample data from our files.
    For initial setup and testing.
    """
    # Add categories
    categories = set()
    for module in all_modules:
        categories.add(module["category"])
    
    category_map = {}  # Maps category names to their IDs
    
    for category_name in categories:
        category = get_category_by_name(db, category_name)
        if not category:
            category = create_category(db, category_name)
        category_map[category_name] = category.id
    
    # Add modules
    module_map = {}  # Maps module names to their IDs
    
    for module_data in all_modules:
        module = get_module_by_name(db, module_data["name"])
        if not module:
            module = create_module(
                db,
                name=module_data["name"],
                description=module_data["description"],
                category_id=category_map[module_data["category"]],
                age_range=module_data["age_range"],
                features=module_data["features"]
            )
        module_map[module_data["name"]] = module.id
    
    # Add lessons and quizzes from learning_content
    for module_name, content in learning_content.items():
        if module_name not in module_map:
            # Skip if module doesn't exist in our data
            continue
        
        module_id = module_map[module_name]
        
        # Add lessons
        if "lessons" in content:
            for lesson_data in content["lessons"]:
                create_lesson(
                    db,
                    title=lesson_data["title"],
                    description=lesson_data["description"],
                    module_id=module_id,
                    content_type=lesson_data["content_type"],
                    difficulty=lesson_data["difficulty"],
                    duration_minutes=lesson_data["duration_minutes"],
                    skills=lesson_data["skills"],
                    content=None  # We'd need to add actual content
                )
        
        # Add quizzes
        if "quizzes" in content:
            for quiz_data in content["quizzes"]:
                create_quiz(
                    db,
                    title=quiz_data["title"],
                    module_id=module_id,
                    questions=quiz_data["questions"]
                )
    
    # Add learning paths
    for path_data in learning_paths:
        # Get module IDs for the path
        path_module_ids = []
        for module_name in path_data["modules"]:
            if module_name in module_map:
                path_module_ids.append(module_map[module_name])
        
        if path_module_ids:
            create_learning_path(
                db,
                name=path_data["name"],
                description=path_data["description"],
                target_age=path_data["target_age"],
                difficulty=path_data["difficulty"],
                estimated_duration_hours=path_data["estimated_duration_hours"],
                modules=path_module_ids
            )