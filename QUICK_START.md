# Quick Start Guide: DSPy for Deep Research

This guide shows you how to use DSPy for answering deep research problems by searching through text from websites.

## 🚀 Quick Start

### 1. Set up your environment
```bash
# Install dependencies
pip install -r requirements.txt

# Set your OpenAI API key
export OPENAI_API_KEY='your-api-key-here'
```

### 2. Run a simple example
```bash
python test_dspy.py
```

### 3. Run the advanced system
```bash
python advanced_research_system.py
```

### 4. Try the example script
```bash
python research_example.py
```

## 📁 Files Overview

- **`test_dspy.py`** - Basic research system with web scraping and DSPy integration
- **`advanced_research_system.py`** - Advanced system with optimization and multi-step reasoning
- **`research_example.py`** - Example usage and demonstrations
- **`requirements.txt`** - All required dependencies
- **`README.md`** - Comprehensive documentation

## 🔍 How It Works

### Basic System (`test_dspy.py`)
1. **Web Scraping**: Extracts clean text from websites
2. **Information Retrieval**: Uses DSPy to find relevant passages
3. **Answer Generation**: Synthesizes information into comprehensive answers

### Advanced System (`advanced_research_system.py`)
1. **Enhanced Scraping**: Better content extraction with titles and headings
2. **Semantic Retrieval**: Relevance scoring and source ranking
3. **Multi-Step Reasoning**: Question analysis → Synthesis → Answer generation
4. **Follow-up Questions**: Automatic generation of related research questions
5. **Confidence Assessment**: Scoring of answer quality

## 💡 Key DSPy Concepts Used

### Signatures
Define what each module should do:
```python
signature = dspy.Signature(
    "query, context -> relevant_passages",
    "Extract relevant passages from context based on query"
)
```

### Modules
Create reusable AI components:
```python
retriever = dspy.ChainOfThought(signature)
```

### Chain of Thought
Enables step-by-step reasoning for better answers.

## 🎯 Example Usage

```python
from test_dspy import DeepResearchSystem

# Initialize system
research_system = DeepResearchSystem()

# Research question
question = "What are the benefits of using DSPy for AI programming?"

# Sources to research
urls = [
    "https://dspy.ai/",
    "https://github.com/stanfordnlp/dspy"
]

# Conduct research
result = research_system.research(question, urls)
print(result['answer'])
```

## 🔧 Customization

### Add Your Own Sources
```python
urls = [
    "https://your-research-source.com",
    "https://another-source.com"
]
```

### Ask Different Questions
```python
questions = [
    "What are the latest trends in AI research?",
    "How do different ML frameworks compare?",
    "What are the ethical implications of LLMs?"
]
```

### Modify DSPy Modules
```python
# Custom signature
custom_signature = dspy.Signature(
    "query, context -> relevant_passages, summary, key_insights",
    "Your custom instruction here"
)
```

## 🎉 Benefits

- **Automated Research**: No manual web scraping needed
- **Semantic Understanding**: DSPy finds relevant information intelligently
- **Comprehensive Answers**: Multi-source synthesis
- **Confidence Scoring**: Know how reliable the answers are
- **Follow-up Questions**: Discover related research areas
- **Modular Design**: Easy to customize and extend

## 🚨 Troubleshooting

### Common Issues
1. **API Key**: Make sure `OPENAI_API_KEY` is set
2. **Dependencies**: Run `pip install -r requirements.txt`
3. **Website Access**: Some sites may block automated requests
4. **Rate Limits**: OpenAI has API rate limits

### Getting Help
- Check the full `README.md` for detailed documentation
- Look at `research_example.py` for more examples
- Modify the code to fit your specific research needs

## 🎯 Next Steps

1. Try the basic system with your own research questions
2. Experiment with the advanced system for better results
3. Customize the DSPy modules for your specific domain
4. Add your own data sources and research questions
5. Explore DSPy's optimization capabilities for even better results

Happy researching! 🔬✨

