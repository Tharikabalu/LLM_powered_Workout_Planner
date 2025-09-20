"""
Database helper functions for workout tracking.
Handles SQLite operations for storing and retrieving workout data.
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
import os

# Database file path
DB_PATH = "workouts.db"

def init_database():
    """
    Initialize the SQLite database and create the workouts table if it doesn't exist.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create workouts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exercise_name TEXT NOT NULL,
            sets INTEGER,
            reps INTEGER,
            weight REAL,
            duration INTEGER,  -- in minutes
            date TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def log_workout(exercise_name: str, sets: Optional[int] = None, 
                reps: Optional[int] = None, weight: Optional[float] = None, 
                duration: Optional[int] = None, date: Optional[str] = None) -> bool:
    """
    Log a workout to the database.
    
    Args:
        exercise_name: Name of the exercise
        sets: Number of sets (optional)
        reps: Number of repetitions (optional)
        weight: Weight used in kg/lbs (optional)
        duration: Duration in minutes (optional)
        date: Date of workout (defaults to today)
    
    Returns:
        bool: True if successful, False otherwise
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO workouts (exercise_name, sets, reps, weight, duration, date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (exercise_name, sets, reps, weight, duration, date))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error logging workout: {e}")
        return False

def get_recent_workouts(limit: int = 5) -> List[Dict]:
    """
    Fetch the most recent workouts from the database.
    
    Args:
        limit: Number of recent workouts to fetch (default: 5)
    
    Returns:
        List of workout dictionaries
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT exercise_name, sets, reps, weight, duration, date
            FROM workouts
            ORDER BY date DESC, created_at DESC
            LIMIT ?
        ''', (limit,))
        
        workouts = []
        for row in cursor.fetchall():
            workout = {
                "exercise_name": row[0],
                "sets": row[1],
                "reps": row[2],
                "weight": row[3],
                "duration": row[4],
                "date": row[5]
            }
            workouts.append(workout)
        
        conn.close()
        return workouts
    except Exception as e:
        print(f"Error fetching workouts: {e}")
        return []

def get_workouts_by_date_range(start_date: str, end_date: str) -> List[Dict]:
    """
    Fetch workouts within a specific date range.
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
    
    Returns:
        List of workout dictionaries
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT exercise_name, sets, reps, weight, duration, date
            FROM workouts
            WHERE date BETWEEN ? AND ?
            ORDER BY date DESC, created_at DESC
        ''', (start_date, end_date))
        
        workouts = []
        for row in cursor.fetchall():
            workout = {
                "exercise_name": row[0],
                "sets": row[1],
                "reps": row[2],
                "weight": row[3],
                "duration": row[4],
                "date": row[5]
            }
            workouts.append(workout)
        
        conn.close()
        return workouts
    except Exception as e:
        print(f"Error fetching workouts by date range: {e}")
        return []

def get_all_workouts() -> List[Dict]:
    """
    Fetch all workouts from the database.
    
    Returns:
        List of all workout dictionaries
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT exercise_name, sets, reps, weight, duration, date
            FROM workouts
            ORDER BY date DESC, created_at DESC
        ''')
        
        workouts = []
        for row in cursor.fetchall():
            workout = {
                "exercise_name": row[0],
                "sets": row[1],
                "reps": row[2],
                "weight": row[3],
                "duration": row[4],
                "date": row[5]
            }
            workouts.append(workout)
        
        conn.close()
        return workouts
    except Exception as e:
        print(f"Error fetching all workouts: {e}")
        return []
