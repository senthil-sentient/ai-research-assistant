#!/usr/bin/env python3
"""
Setup script to configure environment variables for the AI Research Assistant
"""

import os
import sys
from pathlib import Path

def setup_environment():
    """Setup environment variables"""
    
    print("🔧 AI Research Assistant - Environment Setup")
    print("=" * 50)
    
    # Check current environment
    current_api_key = os.getenv("OPENAI_API_KEY")
    
    if current_api_key:
        print("✅ OPENAI_API_KEY is already set in environment")
        print(f"🔑 Current key: {current_api_key[:10]}...{current_api_key[-4:]}")
        
        choice = input("\nDo you want to update it? (y/n): ").lower().strip()
        if choice != 'y':
            print("Environment setup complete!")
            return
    
    # Get API key from user
    print("\n📝 Please enter your OpenAI API key:")
    print("   (You can find it at: https://platform.openai.com/api-keys)")
    
    api_key = input("OpenAI API Key: ").strip()
    
    if not api_key:
        print("❌ No API key provided. Setup cancelled.")
        return
    
    # Create .env file
    env_file = Path(".env")
    
    try:
        # Read existing .env file if it exists
        existing_content = ""
        if env_file.exists():
            existing_content = env_file.read_text()
        
        # Update or add OPENAI_API_KEY
        lines = existing_content.split('\n') if existing_content else []
        updated_lines = []
        key_found = False
        
        for line in lines:
            if line.startswith("OPENAI_API_KEY="):
                updated_lines.append(f"OPENAI_API_KEY={api_key}")
                key_found = True
            else:
                updated_lines.append(line)
        
        if not key_found:
            updated_lines.append(f"OPENAI_API_KEY={api_key}")
        
        # Write back to .env file
        env_file.write_text('\n'.join(updated_lines))
        
        print("✅ Environment variables saved to .env file")
        print("🔑 API key configured successfully!")
        
        # Show instructions for loading
        print("\n📋 To load the environment variables:")
        print("   Option 1: Restart your terminal/shell")
        print("   Option 2: Run: source .env")
        print("   Option 3: Use: python-dotenv (already in requirements.txt)")
        
        print("\n🚀 You can now run:")
        print("   - Streamlit: streamlit run streamlit_research_ui.py")
        print("   - Flask: python app.py")
        
    except Exception as e:
        print(f"❌ Error saving environment variables: {e}")
        print("\n💡 Manual setup:")
        print(f"   export OPENAI_API_KEY='{api_key}'")

def check_environment():
    """Check if environment is properly configured"""
    
    print("🔍 Checking environment configuration...")
    
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment")
        print("💡 Run this script to set it up: python setup_env.py")
        return False
    
    print(f"✅ OPENAI_API_KEY found: {api_key[:10]}...{api_key[-4:]}")
    
    # Check if required packages are installed
    try:
        import streamlit
        import dspy
        import openai
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("💡 Install requirements: pip install -r requirements.txt")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        check_environment()
    else:
        setup_environment()
