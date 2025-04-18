"""
Database models for EduVerse application.
"""
import os
import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, ForeignKey, DateTime, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Get database URL from environment variable
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./eduverse.db")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Create SQLAlchemy engine and session factory
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create declarative base
Base = declarative_base()

class User(Base):
    """User model for EduVerse platform."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(100))
    full_name = Column(String(100))
    age = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    lesson_progress = relationship("LessonProgress", back_populates="user")
    quiz_results = relationship("QuizResult", back_populates="user")
    learning_path_enrollments = relationship("LearningPathEnrollment", back_populates="user")

class Category(Base):
    """Category model for educational modules."""
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    description = Column(Text, nullable=True)
    
    # Relationships
    modules = relationship("Module", back_populates="category")

class Module(Base):
    """Module model representing educational content packages."""
    __tablename__ = "modules"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    description = Column(Text)
    category_id = Column(Integer, ForeignKey("categories.id"))
    age_range = Column(String(50))
    features = Column(JSON, nullable=True)
    
    # Relationships
    category = relationship("Category", back_populates="modules")
    lessons = relationship("Lesson", back_populates="module")
    quizzes = relationship("Quiz", back_populates="module")

class Lesson(Base):
    """Lesson model for educational content."""
    __tablename__ = "lessons"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    description = Column(Text)
    module_id = Column(Integer, ForeignKey("modules.id"))
    content_type = Column(String(50))  # e.g., "story", "game", "simulation"
    difficulty = Column(String(50))    # e.g., "Beginner", "Intermediate", "Advanced"
    duration_minutes = Column(Integer)
    skills = Column(JSON)  # List of skills covered in this lesson
    content = Column(JSON)  # Lesson content in structured format
    
    # Relationships
    module = relationship("Module", back_populates="lessons")
    progress = relationship("LessonProgress", back_populates="lesson")

class Quiz(Base):
    """Quiz model for assessments."""
    __tablename__ = "quizzes"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    module_id = Column(Integer, ForeignKey("modules.id"))
    description = Column(Text, nullable=True)
    questions = Column(JSON)  # List of questions with options and answers
    
    # Relationships
    module = relationship("Module", back_populates="quizzes")
    results = relationship("QuizResult", back_populates="quiz")

class LearningPath(Base):
    """Learning path model for structured educational journeys."""
    __tablename__ = "learning_paths"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), unique=True, index=True)
    description = Column(Text)
    target_age = Column(String(50))
    difficulty = Column(String(50))
    estimated_duration_hours = Column(Integer)
    modules = Column(JSON)  # List of module IDs in the learning path
    
    # Relationships
    enrollments = relationship("LearningPathEnrollment", back_populates="learning_path")

class LessonProgress(Base):
    """Track user progress through lessons."""
    __tablename__ = "lesson_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    completed = Column(Boolean, default=False)
    completion_date = Column(DateTime, nullable=True)
    time_spent_minutes = Column(Integer, default=0)
    last_position = Column(JSON, nullable=True)  # Store position in interactive content
    
    # Relationships
    user = relationship("User", back_populates="lesson_progress")
    lesson = relationship("Lesson", back_populates="progress")

class QuizResult(Base):
    """Store results of quiz attempts."""
    __tablename__ = "quiz_results"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    score = Column(Float)  # Percentage score
    completion_date = Column(DateTime, default=datetime.datetime.utcnow)
    answers = Column(JSON, nullable=True)  # User's answers to questions
    
    # Relationships
    user = relationship("User", back_populates="quiz_results")
    quiz = relationship("Quiz", back_populates="results")

class Message(Base):
    """Store chat messages between parents and teachers."""
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"))
    receiver_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    read = Column(Boolean, default=False)
    
    # Relationships
    sender = relationship("User", foreign_keys=[sender_id])
    receiver = relationship("User", foreign_keys=[receiver_id])

class Conference(Base):
    """Store virtual conference schedules."""
    __tablename__ = "conferences"
    
    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("users.id"))
    parent_id = Column(Integer, ForeignKey("users.id"))
    student_id = Column(Integer, ForeignKey("users.id"))
    scheduled_time = Column(DateTime)
    status = Column(String(50))  # "scheduled", "completed", "cancelled"
    notes = Column(Text, nullable=True)
    
    # Relationships
    teacher = relationship("User", foreign_keys=[teacher_id])
    parent = relationship("User", foreign_keys=[parent_id])
    student = relationship("User", foreign_keys=[student_id])

class LearningPathEnrollment(Base):
    """Track user enrollments in learning paths."""
    __tablename__ = "learning_path_enrollments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    learning_path_id = Column(Integer, ForeignKey("learning_paths.id"))
    enrollment_date = Column(DateTime, default=datetime.datetime.utcnow)
    completed = Column(Boolean, default=False)
    completion_date = Column(DateTime, nullable=True)
    progress_percentage = Column(Float, default=0.0)
    
    # Relationships
    user = relationship("User", back_populates="learning_path_enrollments")
    learning_path = relationship("LearningPath", back_populates="enrollments")

# Function to initialize database
def init_db():
    """Initialize the database by creating all tables."""
    Base.metadata.create_all(bind=engine)

# Function to get a database session
def get_db():
    """Get a database session."""
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()