"""
LangChain setup for workout suggestion generation.
Handles LLM chain creation and workout suggestion logic.
"""

import os
from typing import List, Dict
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from dotenv import load_dotenv

from prompts import get_workout_prompt, WORKOUT_PLANNING_SYSTEM_PROMPT
from db import get_recent_workouts

# Load environment variables
load_dotenv()

class WorkoutSuggestionChain:
    """
    LangChain-based workout suggestion generator.
    """
    
    def __init__(self, model_name: str = "gpt-3.5-turbo", temperature: float = 0.7):
        """
        Initialize the workout suggestion chain.
        
        Args:
            model_name: OpenAI model to use
            temperature: Temperature for response generation
        """
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        self.model_name = model_name
        self.temperature = temperature
    
    def format_workout_history(self, workouts: List[Dict]) -> str:
        """
        Format workout history into a readable string for the LLM.
        
        Args:
            workouts: List of workout dictionaries
        
        Returns:
            Formatted string of workout history
        """
        if not workouts:
            return "No previous workouts found."
        
        formatted_workouts = []
        for i, workout in enumerate(workouts, 1):
            workout_str = f"Workout {i} ({workout['date']}):\n"
            workout_str += f"  Exercise: {workout['exercise_name']}\n"
            
            if workout['sets']:
                workout_str += f"  Sets: {workout['sets']}\n"
            if workout['reps']:
                workout_str += f"  Reps: {workout['reps']}\n"
            if workout['weight']:
                workout_str += f"  Weight: {workout['weight']} kg/lbs\n"
            if workout['duration']:
                workout_str += f"  Duration: {workout['duration']} minutes\n"
            
            formatted_workouts.append(workout_str)
        
        return "\n".join(formatted_workouts)
    
    def generate_workout_suggestion(self, fitness_goal: str, user_id: str = "default") -> str:
        """
        Generate a personalized workout suggestion using LangChain.
        
        Args:
            fitness_goal: User's fitness goal (e.g., "strength", "endurance", "fat loss")
            user_id: User identifier (for future multi-user support)
        
        Returns:
            Generated workout suggestion
        """
        try:
            # Get recent workout history
            recent_workouts = get_recent_workouts(limit=5)
            workout_history = self.format_workout_history(recent_workouts)
            
            # Get current date
            from datetime import datetime
            current_date = datetime.now().strftime("%Y-%m-%d")
            
            # Get appropriate prompt template
            prompt_template = get_workout_prompt(fitness_goal)
            
            # Create the chain
            chain = LLMChain(llm=self.llm, prompt=prompt_template)
            
            # Prepare input variables
            input_vars = {
                "system_prompt": WORKOUT_PLANNING_SYSTEM_PROMPT,
                "workout_history": workout_history,
                "fitness_goal": fitness_goal,
                "current_date": current_date
            }
            
            # Generate the suggestion
            response = chain.run(**input_vars)
            
            return response
            
        except Exception as e:
            error_msg = f"Error generating workout suggestion: {str(e)}"
            print(error_msg)
            return f"I apologize, but I encountered an error while generating your workout suggestion. Please make sure your OpenAI API key is properly configured. Error: {str(e)}"
    
    def generate_workout_suggestion_with_custom_history(self, 
                                                      fitness_goal: str, 
                                                      custom_workouts: List[Dict]) -> str:
        """
        Generate workout suggestion with custom workout history.
        
        Args:
            fitness_goal: User's fitness goal
            custom_workouts: Custom list of workouts to use as history
        
        Returns:
            Generated workout suggestion
        """
        try:
            # Format custom workout history
            workout_history = self.format_workout_history(custom_workouts)
            
            # Get current date
            from datetime import datetime
            current_date = datetime.now().strftime("%Y-%m-%d")
            
            # Get appropriate prompt template
            prompt_template = get_workout_prompt(fitness_goal)
            
            # Create the chain
            chain = LLMChain(llm=self.llm, prompt=prompt_template)
            
            # Prepare input variables
            input_vars = {
                "system_prompt": WORKOUT_PLANNING_SYSTEM_PROMPT,
                "workout_history": workout_history,
                "fitness_goal": fitness_goal,
                "current_date": current_date
            }
            
            # Generate the suggestion
            response = chain.run(**input_vars)
            
            return response
            
        except Exception as e:
            error_msg = f"Error generating workout suggestion: {str(e)}"
            print(error_msg)
            return f"I apologize, but I encountered an error while generating your workout suggestion. Please make sure your OpenAI API key is properly configured. Error: {str(e)}"

# Global instance for easy access
workout_chain = WorkoutSuggestionChain()

def get_workout_suggestion(fitness_goal: str, user_id: str = "default") -> str:
    """
    Convenience function to get workout suggestions.
    
    Args:
        fitness_goal: User's fitness goal
        user_id: User identifier
    
    Returns:
        Generated workout suggestion
    """
    return workout_chain.generate_workout_suggestion(fitness_goal, user_id)
