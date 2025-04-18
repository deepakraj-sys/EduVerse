"""
Database initialization script for EduVerse.
Run this script to create database tables and populate with initial data.
"""
import os
from database_models import init_db, get_db
from db_service import populate_sample_data

def initialize_database():
    """Initialize database by creating tables and adding sample data."""
    print("Initializing database...")
    
    # Create all tables
    init_db()
    print("Database tables created.")
    
    # Get database session
    db = get_db()
    
    # Populate with sample data
    populate_sample_data(db)
    print("Sample data populated.")
    
    print("Database initialization complete.")

if __name__ == "__main__":
    # Check if DATABASE_URL environment variable is set
    if not os.environ.get("DATABASE_URL"):
        print("ERROR: DATABASE_URL environment variable not set.")
        exit(1)
    
    # Run initialization
    initialize_database()