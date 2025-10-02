#!/usr/bin/env python3
"""
Simple example demonstrating how to use DSPy for deep research problems
by searching through text from websites.
"""

import os
from test_dspy import DeepResearchSystem
from advanced_research_system import OptimizedResearchSystem

def simple_research_example():
    """Basic research example using the simple system"""
    print("="*60)
    print("SIMPLE RESEARCH EXAMPLE")
    print("="*60)
    
    # Initialize the research system
    research_system = DeepResearchSystem()
    
    # Research question
    question = "What are the main benefits of using DSPy over traditional prompt engineering?"
    
    # Sources to research
    urls = [
        "https://dspy.ai/",
        "https://github.com/stanfordnlp/dspy"
    ]
    
    # Conduct research
    result = research_system.research(question, urls)
    
    print(f"\nQuestion: {result['question']}")
    print(f"\nAnswer:\n{result['answer']}")
    print(f"\nSources: {len(result['sources_used'])}")

def advanced_research_example():
    """Advanced research example with optimization"""
    print("\n" + "="*60)
    print("ADVANCED RESEARCH EXAMPLE")
    print("="*60)
    
    # Initialize the advanced research system
    research_system = OptimizedResearchSystem()
    
    # Research question
    question = "How does DSPy's modular approach improve AI program development?"
    
    # Sources to research
    urls = [
        "https://dspy.ai/",
        "https://dspy.ai/tutorials/",
        "https://github.com/stanfordnlp/dspy"
    ]
    
    # Conduct research with follow-up questions
    result = research_system.research_with_follow_up(question, urls)
    
    print(f"\nQuestion: {result.question}")
    print(f"Confidence Score: {result.confidence_score:.2f}")
    print(f"\nAnswer:\n{result.answer}")
    
    if result.key_findings:
        print(f"\nKey Findings:")
        for i, finding in enumerate(result.key_findings, 1):
            if finding.strip():
                print(f"  {i}. {finding.strip()}")

def custom_research_example():
    """Example of conducting custom research"""
    print("\n" + "="*60)
    print("CUSTOM RESEARCH EXAMPLE")
    print("="*60)
    
    research_system = OptimizedResearchSystem()
    
    # You can research any topic by providing relevant URLs
    question = "What are the latest trends in AI research and development?"
    
    # Example URLs (you would replace these with actual research sources)
    urls = [
        "https://dspy.ai/",  # DSPy as an example of modern AI framework
        "https://github.com/stanfordnlp/dspy"  # Open source AI research
    ]
    
    result = research_system.research(question, urls)
    
    print(f"\nQuestion: {result.question}")
    print(f"\nAnswer:\n{result.answer}")

if __name__ == "__main__":
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Please set your OPENAI_API_KEY environment variable")
        print("   export OPENAI_API_KEY='your-api-key-here'")
        exit(1)
    
    print("🚀 DSPy Research System Examples")
    print("This demonstrates how to use DSPy for deep research by searching through website content.")
    
    try:
        # Run examples
        simple_research_example()
        advanced_research_example()
        custom_research_example()
        
        print("\n✅ All examples completed successfully!")
        print("\n💡 Key Benefits of this DSPy Research System:")
        print("   • Automated web scraping and content extraction")
        print("   • Semantic information retrieval using DSPy modules")
        print("   • Multi-step reasoning for comprehensive answers")
        print("   • Relevance scoring and source ranking")
        print("   • Follow-up question generation")
        print("   • Confidence assessment")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        print("Make sure you have installed all dependencies:")
        print("   pip install -r requirements.txt")

