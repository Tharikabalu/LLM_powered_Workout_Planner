# LLM-Powered Workout Tracker

A minimal workout tracker with AI-powered suggestions using LangChain and FastAPI. This application allows you to log your workouts and get personalized workout suggestions based on your fitness goals and workout history.

## Features

* **Modern Web Interface**: Beautiful, responsive frontend with intuitive navigation
* **Workout Logging**: Log exercises with sets, reps, weight, and duration
* **AI-Powered Suggestions**: Get personalized workout recommendations using OpenAI GPT
* **Workout History**: Track and view your past workouts with detailed statistics
* **Goal-Based Planning**: Different workout strategies for strength, endurance, and fat loss
* **Real-time Dashboard**: View workout statistics and recent activity
* **REST API**: Clean FastAPI endpoints for easy integration

## Tech Stack

* **Backend**: FastAPI (Python)
* **Database**: SQLite (lightweight, no setup required)
* **AI/LLM**: LangChain + OpenAI GPT
* **Data Validation**: Pydantic models

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Copy the example environment file and add your OpenAI API key:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=your_actual_api_key_here
```

### 3. Run the Application

> The app automatically serves the frontend if a `frontend/` directory exists with `index.html`, `styles.css`, and `script.js`.

**Option A (recommended for development): Run with Uvicorn (auto-reload)**

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

**Option B: Run the app module directly (alternate, uses the `if __name__ == "__main__"` block)**

```bash
python app.py
```

**Option C: Using the run script**

```bash
python run.py
```

The application will be available at:

* **Frontend**: `http://localhost:8000` (if `frontend/` exists)
* **API Documentation**: `http://localhost:8000/docs` (interactive API docs)
* **API Base URL**: `http://localhost:8000` (for programmatic access)

## API Endpoints

### Core Endpoints

* `POST /log_workout` - Log a new workout
* `POST /get_suggestions` - Get AI-powered workout suggestions
* `GET /workouts/recent` - Get recent workouts
* `GET /workouts/all` - Get all workouts
* `GET /workouts/stats` - Get workout statistics

### Example Usage

#### Log a Workout

```bash
curl -X POST "http://localhost:8000/log_workout" \
  -H "Content-Type: application/json" \
  -d '{
    "exercise_name": "Bench Press",
    "sets": 3,
    "reps": 10,
    "weight": 135.0
  }'
```

#### Get Workout Suggestions

```bash
curl -X POST "http://localhost:8000/get_suggestions" \
  -H "Content-Type: application/json" \
  -d '{
    "fitness_goal": "strength building"
  }'
```

## Project Structure

```
LLM_powered_Workout_Planner/
├── app.py                    # FastAPI application with routes
├── db.py                     # SQLite database helper functions
├── llm.py                    # LangChain setup for workout suggestions
├── prompts.py                # Modular prompt templates
├── requirements.txt          # Python dependencies
├── env_template.txt          # Environment variables template
├── run.py                    # Basic startup script
├── test_app.py               # Test script for API endpoints
├── frontend/                 # Frontend web interface (optional)
│   ├── index.html            # Main HTML file
│   ├── styles.css            # Modern CSS styling
│   └── script.js             # JavaScript functionality
└── README.md                 # This file
```

## How It Works

### Frontend Interface

1. **Dashboard**: View workout statistics, recent activity, and quick overview
2. **Log Workout**: Simple form to record exercise sessions with all details
3. **History**: Browse all past workouts organized by date
4. **AI Suggestions**: Get personalized workout recommendations based on your goals

### Backend Processing

1. **Workout Logging**: Data is sent to FastAPI backend and stored in SQLite
2. **Data Storage**: Workouts are stored with exercise details, sets, reps, weight, duration
3. **AI Analysis**: When requesting suggestions, the system:

   * Fetches recent workout history (last 5 workouts)
   * Formats the data for the LLM
   * Uses LangChain with OpenAI GPT to generate personalized suggestions
   * Considers the user's fitness goal (strength, endurance, fat loss)

## Frontend Features

### Dashboard

* **Statistics Overview**: Total workouts, unique exercises, total duration, last workout date
* **Recent Activity**: Quick view of your last 5 workouts
* **Real-time Updates**: Statistics update automatically when you log new workouts

### Workout Logging

* **Simple Form**: Easy-to-use form with all workout fields
* **Smart Defaults**: Today's date pre-filled, optional fields clearly marked
* **Validation**: Client-side validation with helpful error messages
* **Success Feedback**: Toast notifications confirm successful logging

### Workout History

* **Chronological View**: All workouts organized by date
* **Detailed Information**: Sets, reps, weight, duration for each exercise
* **Load Options**: View recent workouts or load all historical data
* **Responsive Design**: Works perfectly on desktop and mobile

### AI Suggestions

* **Goal Selection**: Choose from strength, endurance, fat loss, and more
* **Personalized Recommendations**: Based on your actual workout history
* **Detailed Plans**: Complete workout suggestions with sets, reps, and tips
* **Context Aware**: Considers your recent activity and progression

## Customization

### Adding New Fitness Goals

Edit `prompts.py` to add new prompt templates for different fitness goals:

```python
CUSTOM_GOAL_PROMPT = PromptTemplate(
    input_variables=["workout_history", "current_date"],
    template="Your custom prompt here..."
)
```

### Modifying the LLM Model

Update the model in `llm.py`:

```python
workout_chain = WorkoutSuggestionChain(
    model_name="gpt-4",  # or any other OpenAI model
    temperature=0.5
)
```

## Development

### Running in Development Mode

Prefer this during development:

```bash
uvicorn app:app --reload
```

Alternate (works as well):

```bash
python app.py
```

### Database

The SQLite database (`workouts.db`) is created automatically on first run. The database schema includes:

* `id`: Primary key
* `exercise_name`: Name of the exercise
* `sets`: Number of sets
* `reps`: Number of repetitions
* `weight`: Weight used
* `duration`: Duration in minutes
* `date`: Workout date
* `created_at`: Timestamp

## Future Enhancements

* User authentication and multi-user support
* Workout templates and routines
* Progress tracking and analytics
* Integration with fitness wearables
* Mobile app frontend
* Advanced AI features (form analysis, injury prevention)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.
