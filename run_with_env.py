#!/usr/bin/env python3
"""
Run the Flask app with environment variable setup
"""

import os
import subprocess
import sys

def main():
    """Run Flask app with environment setup"""
    
    print("🚀 Starting AI Research Assistant...")
    
    # Check if API key is set (optional - app will handle it internally)
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("⚠️  OPENAI_API_KEY not found in environment")
        print("💡 The app will attempt to use environment variables automatically")
        print("   If research fails, set: export OPENAI_API_KEY='your-key-here'")
    
    print("🌐 Starting Flask app on http://localhost:8080")
    print("📱 Open your browser and go to the URL above")
    if api_key:
        print(f"✅ API key detected: {api_key[:10]}...{api_key[-4:]}")
    print("\n" + "="*60)
    
    # Start Flask app
    try:
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")

if __name__ == "__main__":
    main()
