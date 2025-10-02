# 🤖 AI Research Assistant - Streamlit UI

A ChatGPT-like interface for conducting deep research using DSPy with flexible reasoning approaches.

## 🚀 Quick Start

### Option 1: Using the Launch Script (Recommended)
```bash
python run_ui.py
```

### Option 2: Direct Streamlit Command
```bash
streamlit run streamlit_research_ui.py
```

## ✨ Features

- **ChatGPT-like Interface**: Clean, modern chat interface with streaming responses
- **Flexible Reasoning**: Choose between Chain of Thought (CoT) and ReAct reasoning approaches
- **Real-time Streaming**: Watch answers generate character by character
- **Multiple Sources**: Research multiple URLs simultaneously
- **Source Attribution**: See which sources were used for each answer
- **Chat History**: Maintain conversation history throughout your session
- **Progress Indicators**: Visual feedback during research process

## 🔧 Configuration

### OpenAI API Key
- Enter your OpenAI API key in the sidebar
- Or set the `OPENAI_API_KEY` environment variable

### Reasoning Approaches
- **Chain of Thought (CoT)**: Sequential reasoning, processes URLs one by one
- **ReAct**: Reasoning + Acting, lets the AI decide which URLs to explore

## 💡 Usage Tips

1. **Enter URLs**: Paste URLs you want to research (one per line)
2. **Ask Questions**: Formulate clear, specific research questions
3. **Choose Reasoning**: Select CoT for systematic analysis or ReAct for adaptive exploration
4. **Watch Streaming**: Enjoy real-time answer generation
5. **Review Sources**: Check which sources contributed to each answer

## 🎨 UI Features

- **Modern Design**: Clean, professional interface
- **Responsive Layout**: Works on desktop and mobile
- **Status Indicators**: Animated progress indicators
- **Chat Bubbles**: Distinct styling for user and AI messages
- **Source Cards**: Highlighted source information
- **Reasoning Display**: Shows thought process for ReAct approach

## 📊 Example Research Questions

- "What does this company do?"
- "What are their main products and services?"
- "How does their pricing model work?"
- "What are their competitive advantages?"
- "What recent news or updates have they announced?"

## 🔍 Technical Details

- Built with Streamlit 1.39.0
- Integrates with your existing `test_dspy.py` research system
- Supports both Chain of Thought and ReAct reasoning
- Real-time web scraping and content analysis
- Streaming text animation for engaging user experience

## 🛠️ Troubleshooting

- **API Key Issues**: Make sure your OpenAI API key is valid and has sufficient credits
- **URL Access**: Some URLs may be blocked or require authentication
- **Memory Usage**: Large research sessions may consume significant memory
- **Network Timeouts**: Adjust timeout settings in the research system if needed

## 🎯 Best Practices

1. **Specific Questions**: Ask focused questions for better results
2. **Quality URLs**: Use authoritative, reliable sources
3. **Reasonable Scope**: Don't overload with too many URLs at once
4. **Review Results**: Always verify information from multiple sources
5. **Save Important Research**: Copy valuable findings to external notes

---

**Happy Researching! 🔍✨**
