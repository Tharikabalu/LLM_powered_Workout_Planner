"""
FastAPI application for the LLM-powered workout tracker.
Provides REST API endpoints for logging workouts and getting AI-powered suggestions.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
import uvicorn
import os

from db import init_database, log_workout, get_recent_workouts, get_all_workouts
from llm import get_workout_suggestion

# Initialize FastAPI app
app = FastAPI(
    title="LLM-Powered Workout Tracker",
    description="A minimal workout tracker with AI-powered suggestions using LangChain",
    version="1.0.0"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response validation
class WorkoutLog(BaseModel):
    """Model for logging a workout."""
    exercise_name: str
    sets: Optional[int] = None
    reps: Optional[int] = None
    weight: Optional[float] = None
    duration: Optional[int] = None  # in minutes
    date: Optional[str] = None  # YYYY-MM-DD format, defaults to today

class WorkoutSuggestionRequest(BaseModel):
    """Model for requesting workout suggestions."""
    fitness_goal: str
    user_id: Optional[str] = "default"

class WorkoutResponse(BaseModel):
    """Model for workout data responses."""
    exercise_name: str
    sets: Optional[int] = None
    reps: Optional[int] = None
    weight: Optional[float] = None
    duration: Optional[int] = None
    date: str

class SuggestionResponse(BaseModel):
    """Model for workout suggestion responses."""
    suggestion: str
    fitness_goal: str
    generated_at: str
    workout_history_count: int

# Mount static files for frontend
if os.path.exists("frontend"):
    app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize the database when the app starts."""
    init_database()

# Serve frontend
@app.get("/")
async def serve_frontend():
    """Serve the frontend application."""
    if os.path.exists("frontend/index.html"):
        return FileResponse("frontend/index.html")
    else:
        return {
            "message": "LLM-Powered Workout Tracker API",
            "status": "healthy",
            "version": "1.0.0",
            "note": "Frontend not found. Please ensure frontend files are in the 'frontend' directory."
        }

# Serve CSS file
@app.get("/styles.css")
async def serve_css():
    """Serve the CSS file."""
    if os.path.exists("frontend/styles.css"):
        return FileResponse("frontend/styles.css", media_type="text/css")
    else:
        raise HTTPException(status_code=404, detail="CSS file not found")

# Serve JavaScript file
@app.get("/script.js")
async def serve_js():
    """Serve the JavaScript file."""
    if os.path.exists("frontend/script.js"):
        return FileResponse("frontend/script.js", media_type="application/javascript")
    else:
        raise HTTPException(status_code=404, detail="JavaScript file not found")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Log workout endpoint
@app.post("/log_workout", response_model=Dict[str, str])
async def log_workout_endpoint(workout: WorkoutLog):
    """
    Log a workout to the database.
    
    Args:
        workout: Workout data to log
    
    Returns:
        Success message with workout details
    """
    try:
        # Log the workout
        success = log_workout(
            exercise_name=workout.exercise_name,
            sets=workout.sets,
            reps=workout.reps,
            weight=workout.weight,
            duration=workout.duration,
            date=workout.date
        )
        
        if success:
            return {
                "message": "Workout logged successfully",
                "exercise": workout.exercise_name,
                "date": workout.date or datetime.now().strftime("%Y-%m-%d")
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to log workout")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error logging workout: {str(e)}")

# Get workout suggestions endpoint
@app.post("/get_suggestions", response_model=SuggestionResponse)
async def get_workout_suggestions(request: WorkoutSuggestionRequest):
    """
    Get AI-powered workout suggestions based on user's history and goals.
    
    Args:
        request: Request containing fitness goal and user ID
    
    Returns:
        Personalized workout suggestion
    """
    try:
        # Get recent workout history for context
        recent_workouts = get_recent_workouts(limit=5)
        
        # Generate workout suggestion using LangChain
        suggestion = get_workout_suggestion(
            fitness_goal=request.fitness_goal,
            user_id=request.user_id
        )
        
        return SuggestionResponse(
            suggestion=suggestion,
            fitness_goal=request.fitness_goal,
            generated_at=datetime.now().isoformat(),
            workout_history_count=len(recent_workouts)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating suggestion: {str(e)}")

# Get recent workouts endpoint
@app.get("/workouts/recent", response_model=List[WorkoutResponse])
async def get_recent_workouts_endpoint(limit: int = 5):
    """
    Get recent workouts from the database.
    
    Args:
        limit: Number of recent workouts to fetch (default: 5)
    
    Returns:
        List of recent workouts
    """
    try:
        workouts = get_recent_workouts(limit=limit)
        return [WorkoutResponse(**workout) for workout in workouts]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching workouts: {str(e)}")

# Get all workouts endpoint
@app.get("/workouts/all", response_model=List[WorkoutResponse])
async def get_all_workouts_endpoint():
    """
    Get all workouts from the database.
    
    Returns:
        List of all workouts
    """
    try:
        workouts = get_all_workouts()
        return [WorkoutResponse(**workout) for workout in workouts]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching all workouts: {str(e)}")

# Get workout statistics endpoint
@app.get("/workouts/stats")
async def get_workout_stats():
    """
    Get basic workout statistics.
    
    Returns:
        Dictionary with workout statistics
    """
    try:
        all_workouts = get_all_workouts()
        
        if not all_workouts:
            return {
                "total_workouts": 0,
                "unique_exercises": 0,
                "message": "No workouts found"
            }
        
        # Calculate statistics
        total_workouts = len(all_workouts)
        unique_exercises = len(set(workout["exercise_name"] for workout in all_workouts))
        
        # Get most recent workout date
        most_recent_date = max(workout["date"] for workout in all_workouts)
        
        # Calculate total duration if available
        total_duration = sum(workout["duration"] for workout in all_workouts if workout["duration"])
        
        return {
            "total_workouts": total_workouts,
            "unique_exercises": unique_exercises,
            "most_recent_workout": most_recent_date,
            "total_duration_minutes": total_duration,
            "average_workouts_per_week": round(total_workouts / max(1, len(set(workout["date"] for workout in all_workouts))), 2)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating stats: {str(e)}")

if __name__ == "__main__":
    # Run the application
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload for development
        log_level="info"
    )
