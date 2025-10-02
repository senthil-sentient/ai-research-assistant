# Flexible DSPy Reasoning Approaches Guide

This guide explains how to use both **ChainOfThought** and **ReAct** reasoning approaches in your DSPy research systems.

## Overview

Your research systems now support two different reasoning approaches:

- **ChainOfThought (CoT)**: Step-by-step reasoning without explicit actions
- **ReAct**: Reasoning with explicit thought-action loops

## Quick Start

### Basic System

```python
from test_dspy import DeepResearchSystem

# ChainOfThought approach (default)
cot_system = DeepResearchSystem(reasoning_approach="cot")
result = cot_system.research("Your question here", ["url1", "url2"])

# ReAct approach
react_system = DeepResearchSystem(reasoning_approach="react")
result = react_system.research("Your question here", ["url1", "url2"])
```

### Advanced System

```python
from advanced_research_system import OptimizedResearchSystem

# ChainOfThought approach
cot_advanced = OptimizedResearchSystem(reasoning_approach="cot")
result = cot_advanced.research("Your question here", ["url1", "url2"])

# ReAct approach
react_advanced = OptimizedResearchSystem(reasoning_approach="react")
result = react_advanced.research("Your question here", ["url1", "url2"])
```

## When to Use Each Approach

### ChainOfThought (CoT)
- **Best for**: Straightforward reasoning tasks
- **Characteristics**: 
  - Direct step-by-step thinking
  - Faster processing
  - Less verbose output
  - Good for simple Q&A tasks

### ReAct
- **Best for**: Complex multi-step reasoning
- **Characteristics**:
  - Explicit thought-action loops
  - More detailed reasoning process
  - Better for complex problem-solving
  - Provides both `thought` and `action` outputs

## Output Differences

### ChainOfThought Output
```python
{
    'answer': 'Your answer here',
    'reasoning_approach': 'cot',
    'sources_used': ['url1', 'url2'],
    'research_context': [...]
}
```

### ReAct Output
```python
{
    'answer': 'Your answer here',
    'reasoning_approach': 'react',
    'sources_used': ['url1', 'url2'],
    'research_context': [...],
    'additional_info': {
        'answer': 'Your answer here',
        'thought': 'Step-by-step thinking process',
        'action': 'Actions taken during reasoning',
        'reasoning_approach': 'react'
    }
}
```

## Example Usage

Run the example script to see both approaches in action:

```bash
python flexible_reasoning_example.py
```

This will demonstrate:
- Basic system with both approaches
- Advanced system with both approaches
- Side-by-side comparison
- Access to ReAct's thought and action outputs

## Individual Module Usage

You can also use the reasoning approaches in individual modules:

```python
from test_dspy import ResearchRetriever, ResearchAnswerer

# Retriever with ReAct
retriever = ResearchRetriever(reasoning_approach="react")
retrieved_info = retriever.forward("query", ["url1", "url2"])

# Answerer with ChainOfThought
answerer = ResearchAnswerer(reasoning_approach="cot")
answer = answerer.forward("question", research_context)
```

## Configuration

Both approaches use the same DSPy configuration:

```python
import dspy
import os

# Configure DSPy (already done in your files)
lm = dspy.LM("openai/gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))
dspy.configure(lm=lm)
```

## Tips

1. **Start with CoT** for simple tasks
2. **Use ReAct** when you need more detailed reasoning
3. **Compare outputs** to see which works better for your use case
4. **Access ReAct details** through `additional_info` in the results
5. **Mix and match** - use different approaches for different parts of your pipeline

## Advanced Features

The advanced system includes:
- Multi-step reasoning with both approaches
- Semantic retrieval with flexible reasoning
- Question analysis with thought-action loops (ReAct)
- Information synthesis with explicit reasoning steps
- Confidence scoring for both approaches

Happy researching! 🧠🔍
