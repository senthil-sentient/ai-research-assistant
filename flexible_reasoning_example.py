#!/usr/bin/env python3
"""
Example demonstrating flexible reasoning approaches in DSPy research systems.
This script shows how to use both ChainOfThought and ReAct approaches.
"""

import os
from test_dspy import DeepResearchSystem
from advanced_research_system import OptimizedResearchSystem

def test_flexible_reasoning():
    """Test both ChainOfThought and ReAct approaches"""
    
    # Example research question
    question = "What are the key features of IDFC First Bank's salary account?"
    
    # URLs to research
    urls = [
        "https://www.idfcfirstbank.com/personal-banking/accounts/salary-account",
        "https://www.idfcfirstbank.com/personal-banking/accounts/current-account"
    ]
    
    print("="*80)
    print("FLEXIBLE DSPy REASONING APPROACHES DEMONSTRATION")
    print("="*80)
    
    # Test basic system with ChainOfThought
    print("\n🧠 Testing Basic System with ChainOfThought...")
    cot_basic = DeepResearchSystem(reasoning_approach="cot")
    cot_result = cot_basic.research(question, urls)
    
    print(f"\nChainOfThought Answer:\n{cot_result['answer']}")
    print(f"Reasoning approach used: {cot_result['reasoning_approach']}")
    
    # Test basic system with ReAct
    print("\n🧠 Testing Basic System with ReAct...")
    react_basic = DeepResearchSystem(reasoning_approach="react")
    react_result = react_basic.research(question, urls)
    
    print(f"\nReAct Answer:\n{react_result['answer']}")
    print(f"Reasoning approach used: {react_result['reasoning_approach']}")
    
    # Show additional ReAct information
    if react_result['additional_info'].get('thought'):
        print(f"\nReAct Thought Process:\n{react_result['additional_info']['thought']}")
    
    if react_result['additional_info'].get('action'):
        print(f"\nReAct Actions:\n{react_result['additional_info']['action']}")
    
    # Test advanced system with ChainOfThought
    print("\n🧠 Testing Advanced System with ChainOfThought...")
    cot_advanced = OptimizedResearchSystem(reasoning_approach="cot")
    cot_advanced_result = cot_advanced.research(question, urls)
    
    print(f"\nAdvanced ChainOfThought Answer:\n{cot_advanced_result.answer}")
    print(f"Confidence Score: {cot_advanced_result.confidence_score}")
    
    # Test advanced system with ReAct
    print("\n🧠 Testing Advanced System with ReAct...")
    react_advanced = OptimizedResearchSystem(reasoning_approach="react")
    react_advanced_result = react_advanced.research(question, urls)
    
    print(f"\nAdvanced ReAct Answer:\n{react_advanced_result.answer}")
    print(f"Confidence Score: {react_advanced_result.confidence_score}")
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print("✅ ChainOfThought: Good for straightforward reasoning tasks")
    print("✅ ReAct: Better for complex multi-step reasoning with explicit actions")
    print("✅ Both approaches are now available in your research systems!")
    print("✅ You can choose the best approach based on your specific use case")

def compare_approaches():
    """Compare the two approaches side by side"""
    
    question = "What are the benefits of having a salary account?"
    urls = ["https://www.idfcfirstbank.com/personal-banking/accounts/salary-account"]
    
    print("\n" + "="*80)
    print("SIDE-BY-SIDE COMPARISON")
    print("="*80)
    
    # Initialize both systems
    cot_system = DeepResearchSystem(reasoning_approach="cot")
    react_system = DeepResearchSystem(reasoning_approach="react")
    
    # Get results
    cot_result = cot_system.research(question, urls)
    react_result = react_system.research(question, urls)
    
    print(f"\nQuestion: {question}")
    print(f"\nChainOfThought Approach:")
    print(f"Answer: {cot_result['answer'][:200]}...")
    
    print(f"\nReAct Approach:")
    print(f"Answer: {react_result['answer'][:200]}...")
    
    if react_result['additional_info'].get('thought'):
        print(f"\nReAct Thought: {react_result['additional_info']['thought'][:150]}...")

if __name__ == "__main__":
    # Check if API key is available
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Please set your OPENAI_API_KEY environment variable")
        exit(1)
    
    # Run the demonstrations
    test_flexible_reasoning()
    compare_approaches()
