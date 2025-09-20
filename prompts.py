"""
Prompt templates for the LLM-powered workout planner.
Contains modular prompt templates for different workout planning scenarios.
"""

from langchain.prompts import PromptTemplate

# System prompt for workout planning
WORKOUT_PLANNING_SYSTEM_PROMPT = """
You are a knowledgeable and encouraging personal fitness coach. Your role is to analyze a user's workout history and provide personalized, actionable workout suggestions based on their fitness goals.

Key principles:
- Always consider the user's past workout patterns and progression
- Provide specific, measurable recommendations
- Consider recovery time and workout balance
- Keep suggestions realistic and achievable
- Include proper form reminders when relevant
- Suggest appropriate rest periods between exercises

Your suggestions should be:
1. Specific with sets, reps, and weights when applicable
2. Progressive (building on previous workouts)
3. Balanced (targeting different muscle groups)
4. Safe and injury-prevention focused
5. Motivating and encouraging

Format your response in a clear, structured way that's easy to follow.
"""

# Main workout suggestion prompt template
WORKOUT_SUGGESTION_PROMPT = PromptTemplate(
    input_variables=["workout_history", "fitness_goal", "current_date"],
    template="""
{system_prompt}

User's Fitness Goal: {fitness_goal}
Current Date: {current_date}

Recent Workout History (last 5 workouts):
{workout_history}

Based on the user's workout history and fitness goal, provide a personalized workout suggestion for today. 

Consider:
- What exercises they've been doing recently
- Their progression patterns
- Recovery needs
- Goal alignment
- Workout variety and balance

Provide a structured workout plan with:
1. Warm-up recommendations
2. Main exercises with specific sets, reps, and weight suggestions
3. Cool-down suggestions
4. Any specific form tips or modifications
5. Rest day recommendations if needed

Keep the workout focused, achievable, and aligned with their goals.
"""
)

# Alternative prompt for strength-focused goals
STRENGTH_FOCUSED_PROMPT = PromptTemplate(
    input_variables=["workout_history", "current_date"],
    template="""
{system_prompt}

User's Fitness Goal: Strength Building
Current Date: {current_date}

Recent Workout History (last 5 workouts):
{workout_history}

Design a strength-focused workout that emphasizes:
- Progressive overload
- Compound movements
- Adequate rest between sets (2-3 minutes)
- Focus on form over speed
- Gradual weight progression

Provide specific recommendations for:
1. Compound exercises (squats, deadlifts, bench press, etc.)
2. Accessory exercises
3. Set and rep schemes (typically 3-5 sets of 3-8 reps for strength)
4. Weight progression suggestions
5. Rest periods
"""
)

# Alternative prompt for endurance/cardio goals
ENDURANCE_FOCUSED_PROMPT = PromptTemplate(
    input_variables=["workout_history", "current_date"],
    template="""
{system_prompt}

User's Fitness Goal: Endurance/Cardio
Current Date: {current_date}

Recent Workout History (last 5 workouts):
{workout_history}

Design an endurance-focused workout that emphasizes:
- Cardiovascular fitness
- Muscular endurance
- Longer duration activities
- Heart rate zones
- Recovery between exercises

Provide specific recommendations for:
1. Cardio activities (running, cycling, rowing, etc.)
2. Circuit training exercises
3. Duration and intensity levels
4. Heart rate targets
5. Active recovery periods
"""
)

# Alternative prompt for fat loss goals
FAT_LOSS_FOCUSED_PROMPT = PromptTemplate(
    input_variables=["workout_history", "current_date"],
    template="""
{system_prompt}

User's Fitness Goal: Fat Loss
Current Date: {current_date}

Recent Workout History (last 5 workouts):
{workout_history}

Design a fat loss-focused workout that emphasizes:
- High-intensity interval training (HIIT)
- Compound movements for calorie burn
- Metabolic conditioning
- Strength training to preserve muscle
- Active recovery

Provide specific recommendations for:
1. HIIT exercises and timing
2. Strength exercises with higher reps
3. Circuit training format
4. Work-to-rest ratios
5. Total workout duration
"""
)

# Function to get the appropriate prompt based on fitness goal
def get_workout_prompt(fitness_goal: str) -> PromptTemplate:
    """
    Get the appropriate prompt template based on the user's fitness goal.
    
    Args:
        fitness_goal: The user's stated fitness goal
    
    Returns:
        PromptTemplate: The appropriate prompt template
    """
    goal_lower = fitness_goal.lower()
    
    if "strength" in goal_lower or "muscle" in goal_lower:
        return STRENGTH_FOCUSED_PROMPT
    elif "endurance" in goal_lower or "cardio" in goal_lower:
        return ENDURANCE_FOCUSED_PROMPT
    elif "fat" in goal_lower or "weight loss" in goal_lower or "lose" in goal_lower:
        return FAT_LOSS_FOCUSED_PROMPT
    else:
        return WORKOUT_SUGGESTION_PROMPT
