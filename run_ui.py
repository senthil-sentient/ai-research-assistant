#!/usr/bin/env python3
"""
Launch script for the AI Research Assistant Streamlit UI
"""

import subprocess
import sys
import os

def main():
    """Launch the Streamlit application"""
    
    # Check if streamlit is installed
    try:
        import streamlit
        print("✅ Streamlit is installed")
    except ImportError:
        print("❌ Streamlit not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit==1.50.0"])
        print("✅ Streamlit installed successfully")
    
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY environment variable not set")
        print("   You can set it in the Streamlit UI or as an environment variable")
    
    print("\n🚀 Starting AI Research Assistant...")
    print("📱 The app will open in your default browser")
    print("🔗 If it doesn't open automatically, go to: http://localhost:8501")
    print("\n💡 Tips:")
    print("   - Enter your OpenAI API key in the sidebar")
    print("   - Choose between Chain of Thought or ReAct reasoning")
    print("   - Enter URLs and your research question")
    print("   - Enjoy ChatGPT-like streaming responses!")
    print("\n" + "="*60)
    
    # Launch Streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "streamlit_research_ui.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 Shutting down AI Research Assistant...")
    except Exception as e:
        print(f"\n❌ Error launching Streamlit: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
