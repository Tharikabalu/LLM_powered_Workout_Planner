# LLM-Powered Workout Tracker

A minimal workout tracker with AI-powered suggestions using LangChain and FastAPI. This application allows you to log your workouts and get personalized workout suggestions based on your fitness goals and workout history.

## Features

- **Workout Logging**: Log exercises with sets, reps, weight, and duration
- **AI-Powered Suggestions**: Get personalized workout recommendations using OpenAI GPT
- **Workout History**: Track and view your past workouts
- **Goal-Based Planning**: Different workout strategies for strength, endurance, and fat loss
- **REST API**: Clean FastAPI endpoints for easy integration

## Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: SQLite (lightweight, no setup required)
- **AI/LLM**: LangChain + OpenAI GPT
- **Data Validation**: Pydantic models

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

```bash
python app.py
```

The API will be available at `http://localhost:8000`

### 4. View API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation.

## API Endpoints

### Core Endpoints

- `POST /log_workout` - Log a new workout
- `POST /get_suggestions` - Get AI-powered workout suggestions
- `GET /workouts/recent` - Get recent workouts
- `GET /workouts/all` - Get all workouts
- `GET /workouts/stats` - Get workout statistics

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
├── app.py              # FastAPI application with routes
├── db.py               # SQLite database helper functions
├── llm.py              # LangChain setup for workout suggestions
├── prompts.py          # Modular prompt templates
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
└── README.md          # This file
```

## How It Works

1. **Workout Logging**: Users log workouts through the `/log_workout` endpoint
2. **Data Storage**: Workouts are stored in SQLite database with exercise details
3. **AI Analysis**: When requesting suggestions, the system:
   - Fetches recent workout history (last 5 workouts)
   - Formats the data for the LLM
   - Uses LangChain with OpenAI GPT to generate personalized suggestions
   - Considers the user's fitness goal (strength, endurance, fat loss)

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

The app includes auto-reload for development:

```bash
python app.py
```

### Database

The SQLite database (`workouts.db`) is created automatically on first run. The database schema includes:

- `id`: Primary key
- `exercise_name`: Name of the exercise
- `sets`: Number of sets
- `reps`: Number of repetitions
- `weight`: Weight used
- `duration`: Duration in minutes
- `date`: Workout date
- `created_at`: Timestamp

## Future Enhancements

- User authentication and multi-user support
- Workout templates and routines
- Progress tracking and analytics
- Integration with fitness wearables
- Mobile app frontend
- Advanced AI features (form analysis, injury prevention)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.