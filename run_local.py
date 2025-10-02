#!/usr/bin/env python3
"""
Local development server for the AI Research Assistant
"""

import subprocess
import sys
import os

def main():
    """Launch the Flask application locally"""
    
    # Check if Flask is installed
    try:
        import flask
        print("✅ Flask is installed")
    except ImportError:
        print("❌ Flask not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask==3.0.0"])
        print("✅ Flask installed successfully")
    
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY environment variable not set")
        print("   You can set it in the web interface or as an environment variable")
        print("   Example: export OPENAI_API_KEY='your-key-here'")
    
    print("\n🚀 Starting AI Research Assistant locally...")
    print("📱 The app will be available at: http://localhost:5000")
    print("\n💡 Tips:")
    print("   - Enter your OpenAI API key in the sidebar")
    print("   - Choose between Chain of Thought or ReAct reasoning")
    print("   - Enter URLs and your research question")
    print("   - Enjoy the ChatGPT-like interface!")
    print("\n" + "="*60)
    
    # Launch Flask app
    try:
        subprocess.run([
            sys.executable, "app.py"
        ])
    except KeyboardInterrupt:
        print("\n👋 Shutting down AI Research Assistant...")
    except Exception as e:
        print(f"\n❌ Error launching Flask app: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
