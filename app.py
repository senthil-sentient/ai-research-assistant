# Import Vercel configuration FIRST - this sets up the environment
import vercel_config

import os
import json
import time
from flask import Flask, render_template, request, jsonify, session
import uuid

# Configure DSPy for serverless deployment BEFORE importing test_dspy
from dspy_config import configure_dspy_for_serverless
configure_dspy_for_serverless()

# Now import the research system
from test_dspy import DeepResearchSystem

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Initialize session storage for chat history
chat_sessions = {}

def get_session_id():
    """Get or create session ID"""
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return session['session_id']

def get_chat_history():
    """Get chat history for current session"""
    session_id = get_session_id()
    if session_id not in chat_sessions:
        chat_sessions[session_id] = []
    return chat_sessions[session_id]

def add_to_chat_history(message_type, content, **kwargs):
    """Add message to chat history"""
    chat_history = get_chat_history()
    message = {
        'type': message_type,
        'content': content,
        'timestamp': time.time(),
        **kwargs
    }
    chat_history.append(message)
    return message

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat requests"""
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        urls = data.get('urls', [])
        reasoning_approach = data.get('reasoning_approach', 'cot')
        
        if not question:
            return jsonify({'error': 'Please enter a research question'}), 400
        
        if not urls:
            return jsonify({'error': 'Please enter at least one URL'}), 400
        
        # Add user message to chat history
        add_to_chat_history('user', question, urls=urls, reasoning_approach=reasoning_approach)
        
        # Initialize research system
        research_system = DeepResearchSystem(reasoning_approach=reasoning_approach)
        
        # Conduct research
        result = research_system.research(question, urls)
        
        # Add research result to chat history
        add_to_chat_history('research_result', result)
        
        return jsonify({
            'success': True,
            'result': result
        })
        
    except Exception as e:
        return jsonify({'error': f'Research failed: {str(e)}'}), 500

@app.route('/api/chat/history', methods=['GET'])
def get_chat_history_api():
    """Get chat history for current session"""
    return jsonify(get_chat_history())

@app.route('/api/chat/clear', methods=['POST'])
def clear_chat_history():
    """Clear chat history for current session"""
    session_id = get_session_id()
    chat_sessions[session_id] = []
    return jsonify({'success': True})

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'AI Research Assistant is running'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))  # Changed default port to 8080
    app.run(host='0.0.0.0', port=port, debug=False)
