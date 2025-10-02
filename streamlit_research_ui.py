import streamlit as st
import time
import os
from typing import List, Dict, Any
import json
from test_dspy import DeepResearchSystem

# Configure Streamlit page
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for ChatGPT-like styling
st.markdown("""
<style>
    .main-header {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 2.5rem;
        font-weight: 600;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .chat-message {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
        max-width: 85%;
        word-wrap: break-word;
    }
    
    .user-message {
        background-color: #e3f2fd;
        margin-left: auto;
        margin-right: 0;
        border: 1px solid #bbdefb;
    }
    
    .assistant-message {
        background-color: #f5f5f5;
        margin-left: 0;
        margin-right: auto;
        border: 1px solid #e0e0e0;
    }
    
    .streaming-text {
        font-family: 'JetBrains Mono', 'Consolas', monospace;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    .source-info {
        background-color: #fff3e0;
        border: 1px solid #ffcc02;
        border-radius: 5px;
        padding: 0.5rem;
        margin: 0.5rem 0;
        font-size: 0.85rem;
    }
    
    .reasoning-info {
        background-color: #f3e5f5;
        border: 1px solid #ce93d8;
        border-radius: 5px;
        padding: 0.5rem;
        margin: 0.5rem 0;
        font-size: 0.85rem;
    }
    
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 0.5rem;
    }
    
    .status-researching {
        background-color: #ff9800;
        animation: pulse 1.5s infinite;
    }
    
    .status-thinking {
        background-color: #2196f3;
        animation: pulse 1s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'research_system' not in st.session_state:
        st.session_state.research_system = None
    if 'is_researching' not in st.session_state:
        st.session_state.is_researching = False

def create_streaming_text_effect(text: str, delay: float = 0.03) -> str:
    """Simulate streaming text effect by revealing characters progressively"""
    placeholder = st.empty()
    revealed_text = ""
    
    for char in text:
        revealed_text += char
        placeholder.markdown(f'<div class="chat-message assistant-message"><div class="streaming-text">{revealed_text}</div></div>', unsafe_allow_html=True)
        time.sleep(delay)
    
    return revealed_text

def display_chat_message(message: str, is_user: bool = False, is_streaming: bool = False):
    """Display a chat message with appropriate styling"""
    if is_user:
        st.markdown(f'<div class="chat-message user-message">{message}</div>', unsafe_allow_html=True)
    else:
        if is_streaming:
            return create_streaming_text_effect(message)
        else:
            st.markdown(f'<div class="chat-message assistant-message"><div class="streaming-text">{message}</div></div>', unsafe_allow_html=True)

def display_research_results(result: Dict[str, Any]):
    """Display research results with source information"""
    
    # Main answer
    st.markdown("### 🤖 Research Answer")
    answer_placeholder = st.empty()
    answer_placeholder.markdown(f'<div class="chat-message assistant-message"><div class="streaming-text">{result["answer"]}</div></div>', unsafe_allow_html=True)
    
    # Reasoning approach info
    if result.get('reasoning_approach'):
        approach = result['reasoning_approach'].upper()
        st.markdown(f'<div class="reasoning-info"><strong>🧠 Reasoning Approach:</strong> {approach}</div>', unsafe_allow_html=True)
    
    # Additional reasoning info for ReAct
    if result.get('additional_info'):
        additional = result['additional_info']
        if additional.get('thought'):
            st.markdown("### 💭 Thought Process")
            st.markdown(f'<div class="reasoning-info">{additional["thought"]}</div>', unsafe_allow_html=True)
        
        if additional.get('action'):
            st.markdown("### ⚡ Actions Taken")
            st.markdown(f'<div class="reasoning-info">{additional["action"]}</div>', unsafe_allow_html=True)
    
    # Sources used
    if result.get('sources_used'):
        st.markdown("### 📚 Sources Used")
        for source in result['sources_used']:
            st.markdown(f'<div class="source-info">🔗 {source}</div>', unsafe_allow_html=True)

def research_with_streaming(question: str, urls: List[str], reasoning_approach: str):
    """Conduct research with streaming UI updates"""
    
    # Initialize research system if not exists or if approach changed
    if (st.session_state.research_system is None or 
        st.session_state.research_system.reasoning_approach != reasoning_approach):
        st.session_state.research_system = DeepResearchSystem(reasoning_approach=reasoning_approach)
    
    # Display research status
    status_placeholder = st.empty()
    status_placeholder.markdown(f'''
    <div class="status-indicator status-researching"></div>
    <strong>Researching:</strong> {question}
    ''', unsafe_allow_html=True)
    
    # Simulate research process with status updates
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Step 1: Retrieving information
    status_text.text("🔍 Retrieving information from sources...")
    progress_bar.progress(25)
    time.sleep(1)
    
    # Step 2: Processing with reasoning approach
    status_text.text(f"🧠 Processing with {reasoning_approach.upper()} reasoning...")
    progress_bar.progress(50)
    time.sleep(1)
    
    # Step 3: Analyzing and synthesizing
    status_text.text("🤔 Analyzing and synthesizing information...")
    progress_bar.progress(75)
    time.sleep(1)
    
    # Step 4: Generating answer
    status_text.text("✨ Generating comprehensive answer...")
    progress_bar.progress(100)
    
    # Perform actual research
    try:
        result = st.session_state.research_system.research(question, urls)
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
        status_placeholder.empty()
        
        return result
        
    except Exception as e:
        progress_bar.empty()
        status_text.empty()
        status_placeholder.empty()
        st.error(f"Research failed: {str(e)}")
        return None

def main():
    """Main Streamlit application"""
    
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.markdown('<div class="main-header">🔍 AI Research Assistant</div>', unsafe_allow_html=True)
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Key input
        api_key = st.text_input(
            "OpenAI API Key",
            value=os.getenv("OPENAI_API_KEY", ""),
            type="password",
            help="Enter your OpenAI API key to enable research functionality"
        )
        
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
            st.success("✅ API Key configured")
        else:
            st.warning("⚠️ Please enter your OpenAI API key")
        
        # Reasoning approach selection
        reasoning_approach = st.selectbox(
            "🧠 Reasoning Approach",
            options=["cot", "react"],
            format_func=lambda x: "Chain of Thought" if x == "cot" else "ReAct (Reasoning + Acting)",
            help="Choose the reasoning approach for the AI research system"
        )
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()
        
        # Display chat statistics
        st.header("📊 Chat Statistics")
        st.metric("Messages", len(st.session_state.chat_history))
    
    # Main chat interface
    st.header("💬 Research Chat")
    
    # Display chat history
    for i, message in enumerate(st.session_state.chat_history):
        if message["type"] == "user":
            st.markdown(f'<div class="chat-message user-message"><strong>You:</strong><br>{message["content"]}</div>', unsafe_allow_html=True)
        elif message["type"] == "research_result":
            display_research_results(message["content"])
    
    # Chat input
    st.markdown("---")
    
    # URL input
    st.subheader("📝 Research Sources")
    url_input = st.text_area(
        "Enter URLs (one per line):",
        placeholder="https://example1.com\nhttps://example2.com",
        height=100,
        help="Enter the URLs you want to research, one per line"
    )
    
    # Question input
    question_input = st.text_input(
        "🔍 Research Question:",
        placeholder="What does this company do? What are their main products?",
        help="Enter your research question"
    )
    
    # Research button
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        research_button = st.button(
            "🚀 Start Research",
            type="primary",
            disabled=not (api_key and question_input and url_input),
            use_container_width=True
        )
    
    # Handle research request
    if research_button:
        if not api_key:
            st.error("Please enter your OpenAI API key in the sidebar")
        elif not question_input:
            st.error("Please enter a research question")
        elif not url_input:
            st.error("Please enter at least one URL")
        else:
            # Parse URLs
            urls = [url.strip() for url in url_input.split('\n') if url.strip()]
            
            if not urls:
                st.error("Please enter valid URLs")
            else:
                # Add user message to chat history
                st.session_state.chat_history.append({
                    "type": "user",
                    "content": question_input,
                    "urls": urls,
                    "reasoning_approach": reasoning_approach
                })
                
                # Conduct research
                st.session_state.is_researching = True
                
                try:
                    result = research_with_streaming(question_input, urls, reasoning_approach)
                    
                    if result:
                        # Add research result to chat history
                        st.session_state.chat_history.append({
                            "type": "research_result",
                            "content": result
                        })
                        
                        # Rerun to display results
                        st.rerun()
                    else:
                        st.error("Research failed. Please try again.")
                        
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                finally:
                    st.session_state.is_researching = False

if __name__ == "__main__":
    main()
