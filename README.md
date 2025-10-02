# DSPy Research System

A comprehensive system for conducting deep research by searching through website content using DSPy (Declarative Self-improving Python).

## Overview

This system demonstrates how to use DSPy for answering complex research questions by:
- Automatically scraping and processing content from multiple websites
- Using DSPy's modular approach for semantic information retrieval
- Applying multi-step reasoning to synthesize comprehensive answers
- Providing confidence scores and key findings

## Features

### Basic Research System (`test_dspy.py`)
- **Web Scraping**: Extract clean text content from websites
- **Information Retrieval**: Use DSPy modules to find relevant passages
- **Question Answering**: Generate comprehensive answers from multiple sources

### Advanced Research System (`advanced_research_system.py`)
- **Enhanced Content Extraction**: Better text processing with title and heading extraction
- **Semantic Retrieval**: Relevance scoring and source ranking
- **Multi-Step Reasoning**: Question analysis, synthesis, and answer generation
- **Follow-up Questions**: Automatic generation of related research questions
- **Confidence Assessment**: Scoring of answer quality and reliability

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set your OpenAI API key:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

## Usage

### Basic Usage

```python
from test_dspy import DeepResearchSystem

# Initialize the research system
research_system = DeepResearchSystem()

# Define your research question
question = "What are the key principles of DSPy for AI programming?"

# Provide URLs to research
urls = [
    "https://dspy.ai/",
    "https://github.com/stanfordnlp/dspy"
]

# Conduct research
result = research_system.research(question, urls)

print(f"Answer: {result['answer']}")
```

### Advanced Usage

```python
from advanced_research_system import OptimizedResearchSystem

# Initialize the advanced system
research_system = OptimizedResearchSystem()

# Research with follow-up questions
result = research_system.research_with_follow_up(question, urls)

print(f"Answer: {result.answer}")
print(f"Confidence: {result.confidence_score}")
print(f"Key Findings: {result.key_findings}")
```

### Running Examples

```bash
# Run the example script
python research_example.py

# Run the basic system directly
python test_dspy.py

# Run the advanced system
python advanced_research_system.py
```

## Key Components

### 1. Web Scraping (`WebScraper` / `AdvancedWebScraper`)
- Extracts clean text content from websites
- Handles different content structures and formats
- Provides error handling and content validation

### 2. Information Retrieval (`ResearchRetriever` / `SemanticRetriever`)
- Uses DSPy's `ChainOfThought` for semantic understanding
- Extracts relevant passages based on research queries
- Provides relevance scoring and source ranking

### 3. Answer Generation (`ResearchAnswerer` / `MultiStepAnswerer`)
- Synthesizes information from multiple sources
- Uses multi-step reasoning for comprehensive answers
- Provides confidence assessment and key findings

### 4. Research Orchestration (`DeepResearchSystem` / `OptimizedResearchSystem`)
- Coordinates the entire research pipeline
- Handles error recovery and fallback strategies
- Provides structured output with metadata

## DSPy Integration

This system leverages several key DSPy concepts:

### Signatures
```python
# Define what the module should do
signature = dspy.Signature(
    "query, context -> relevant_passages",
    "Extract relevant passages from context based on query"
)
```

### Modules
```python
# Create reusable AI modules
retriever = dspy.ChainOfThought(signature)
```

### Chain of Thought
- Enables step-by-step reasoning
- Improves answer quality and reliability
- Provides transparency in the reasoning process

## Customization

### Adding New Sources
```python
# Add any website URLs
urls = [
    "https://example.com/research-paper",
    "https://another-site.com/analysis",
    "https://academic-journal.com/study"
]
```

### Custom Research Questions
```python
# Ask any research question
questions = [
    "What are the latest developments in AI safety?",
    "How do different machine learning frameworks compare?",
    "What are the ethical implications of large language models?"
]
```

### Modifying DSPy Modules
```python
# Customize the retrieval signature
custom_signature = dspy.Signature(
    "query, context -> relevant_passages, summary, key_insights",
    "Your custom instruction here"
)
```

## Benefits of Using DSPy

1. **Modularity**: Break down complex research tasks into reusable components
2. **Optimization**: DSPy can automatically optimize prompts and reasoning chains
3. **Composability**: Mix and match different modules for different research needs
4. **Reliability**: Built-in error handling and fallback strategies
5. **Transparency**: Clear reasoning process and confidence scoring

## Example Output

```
🔍 Researching: What are the key principles and benefits of using DSPy for AI programming?
📚 Sources: 3 URLs

📖 Retrieving information from sources...
  ✅ DSPy - Programming—not prompting—LMs (1247 words)
  ✅ stanfordnlp/dspy (892 words)
  ✅ DSPy Tutorials (1156 words)

🔍 Analyzing content for relevance...
📊 Using top 3 most relevant sources:
  1. DSPy - Programming—not prompting—LMs (relevance: 0.95)
  2. DSPy Tutorials (relevance: 0.87)
  3. stanfordnlp/dspy (relevance: 0.82)

🤔 Synthesizing information and generating answer...

Answer: DSPy represents a paradigm shift from traditional prompt engineering to declarative AI programming. The key principles include:

1. **Modular Design**: Instead of writing brittle prompt strings, DSPy allows you to build AI software from natural-language modules that can be composed and reused.

2. **Automatic Optimization**: DSPy's optimizers can automatically tune prompts and weights, improving performance without manual intervention.

3. **Composability**: Modules can be generically composed with different models, inference strategies, or learning algorithms.

4. **Reliability**: The framework makes AI software more reliable, maintainable, and portable across different models and strategies.

The main benefits include faster iteration, better performance through optimization, and the ability to build sophisticated AI systems without extensive prompt engineering expertise.

Confidence Score: 0.89

Key Findings:
- DSPy enables programming AI systems rather than just prompting them
- Automatic optimization reduces the need for manual prompt tuning
- Modular approach improves maintainability and reusability
- Framework supports multiple models and inference strategies
```

## Troubleshooting

### Common Issues

1. **API Key Not Set**
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```

2. **Missing Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Website Access Issues**
   - Some websites may block automated requests
   - Check if the URLs are accessible
   - Consider using different sources

4. **Rate Limiting**
   - OpenAI API has rate limits
   - Consider adding delays between requests
   - Use smaller batches of URLs

## Contributing

Feel free to extend this system with:
- Additional content sources (PDFs, databases, APIs)
- New DSPy modules for specific research tasks
- Enhanced optimization strategies
- Better error handling and recovery

## License

This project is open source and available under the MIT License.

