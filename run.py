#!/usr/bin/env python3
"""
Simple startup script for the LLM-Powered Workout Tracker.
This script handles environment setup and starts the FastAPI server.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_requirements():
    """Check if all required packages are installed."""
    try:
        import fastapi
        import uvicorn
        import langchain
        import langchain_openai
        import dotenv
        import pydantic
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return False

def check_env_file():
    """Check if .env file exists and has OpenAI API key."""
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  .env file not found")
        print("Please create a .env file with your OpenAI API key:")
        print("OPENAI_API_KEY=your_api_key_here")
        return False
    
    # Check if API key is set
    with open(env_file, 'r') as f:
        content = f.read()
        if "your_openai_api_key_here" in content or "OPENAI_API_KEY=" not in content:
            print("⚠️  Please set your OpenAI API key in the .env file")
            return False
    
    print("✅ Environment file configured")
    return True

def main():
    """Main startup function."""
    print("🚀 Starting LLM-Powered Workout Tracker")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check environment
    if not check_env_file():
        print("\nTo get started:")
        print("1. Get an OpenAI API key from: https://platform.openai.com/api-keys")
        print("2. Create a .env file with: OPENAI_API_KEY=your_key_here")
        print("3. Run this script again")
        sys.exit(1)
    
    print("\n🎯 Starting FastAPI server...")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔗 API Base URL: http://localhost:8000")
    print("⏹️  Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Start the FastAPI server
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Goodbye!")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
