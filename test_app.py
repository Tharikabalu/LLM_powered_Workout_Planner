"""
Simple test script to demonstrate the workout tracker functionality.
This script shows how to use the API endpoints programmatically.
"""

import requests
import json
from datetime import datetime

# Base URL for the API
BASE_URL = "http://localhost:8000"

def test_workout_tracker():
    """Test the workout tracker functionality."""
    
    print("🏋️ Testing LLM-Powered Workout Tracker")
    print("=" * 50)
    
    # Test 1: Health check
    print("\n1. Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
        else:
            print("❌ Health check failed")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the server is running on localhost:8000")
        return
    
    # Test 2: Log some sample workouts
    print("\n2. Logging sample workouts...")
    sample_workouts = [
        {
            "exercise_name": "Bench Press",
            "sets": 3,
            "reps": 10,
            "weight": 135.0,
            "date": "2024-01-15"
        },
        {
            "exercise_name": "Squats",
            "sets": 4,
            "reps": 12,
            "weight": 185.0,
            "date": "2024-01-16"
        },
        {
            "exercise_name": "Deadlifts",
            "sets": 3,
            "reps": 8,
            "weight": 225.0,
            "date": "2024-01-17"
        },
        {
            "exercise_name": "Pull-ups",
            "sets": 3,
            "reps": 8,
            "weight": None,
            "date": "2024-01-18"
        },
        {
            "exercise_name": "Overhead Press",
            "sets": 3,
            "reps": 10,
            "weight": 95.0,
            "date": "2024-01-19"
        }
    ]
    
    for workout in sample_workouts:
        try:
            response = requests.post(
                f"{BASE_URL}/log_workout",
                json=workout,
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                print(f"✅ Logged: {workout['exercise_name']}")
            else:
                print(f"❌ Failed to log: {workout['exercise_name']}")
        except Exception as e:
            print(f"❌ Error logging {workout['exercise_name']}: {e}")
    
    # Test 3: Get recent workouts
    print("\n3. Fetching recent workouts...")
    try:
        response = requests.get(f"{BASE_URL}/workouts/recent?limit=3")
        if response.status_code == 200:
            workouts = response.json()
            print(f"✅ Retrieved {len(workouts)} recent workouts:")
            for workout in workouts:
                print(f"   - {workout['exercise_name']} ({workout['date']})")
        else:
            print("❌ Failed to fetch recent workouts")
    except Exception as e:
        print(f"❌ Error fetching workouts: {e}")
    
    # Test 4: Get workout statistics
    print("\n4. Getting workout statistics...")
    try:
        response = requests.get(f"{BASE_URL}/workouts/stats")
        if response.status_code == 200:
            stats = response.json()
            print("✅ Workout Statistics:")
            print(f"   - Total workouts: {stats['total_workouts']}")
            print(f"   - Unique exercises: {stats['unique_exercises']}")
            print(f"   - Most recent: {stats['most_recent_workout']}")
        else:
            print("❌ Failed to fetch statistics")
    except Exception as e:
        print(f"❌ Error fetching stats: {e}")
    
    # Test 5: Get AI workout suggestions
    print("\n5. Getting AI workout suggestions...")
    fitness_goals = ["strength building", "endurance", "fat loss"]
    
    for goal in fitness_goals:
        print(f"\n   Testing goal: {goal}")
        try:
            response = requests.post(
                f"{BASE_URL}/get_suggestions",
                json={"fitness_goal": goal},
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                suggestion = response.json()
                print(f"✅ Got suggestion for {goal}")
                print(f"   Goal: {suggestion['fitness_goal']}")
                print(f"   History count: {suggestion['workout_history_count']}")
                print(f"   Generated at: {suggestion['generated_at']}")
                print(f"   Suggestion preview: {suggestion['suggestion'][:100]}...")
            else:
                print(f"❌ Failed to get suggestion for {goal}")
                print(f"   Status: {response.status_code}")
                print(f"   Response: {response.text}")
        except Exception as e:
            print(f"❌ Error getting suggestion for {goal}: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Test completed!")
    print("\nTo run the API server:")
    print("python app.py")
    print("\nTo view API documentation:")
    print("http://localhost:8000/docs")

if __name__ == "__main__":
    test_workout_tracker()
