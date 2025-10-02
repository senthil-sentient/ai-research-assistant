import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import List, Dict, Any, Optional
import re
import json
from dataclasses import dataclass

# Configure DSPy for serverless deployment
from dspy_config import get_dspy_lm
import dspy

# Configure DSPy
lm = get_dspy_lm()

@dataclass
class ResearchResult:
    """Data class for structured research results"""
    question: str
    answer: str
    sources_used: List[str]
    confidence_score: float
    key_findings: List[str]
    research_context: List[Dict[str, str]]

class AdvancedWebScraper:
    """Enhanced web scraper with better content extraction and filtering"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def extract_text_from_url(self, url: str, max_length: int = 15000) -> Dict[str, Any]:
        """Extract structured content from a URL"""
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(["script", "style", "nav", "footer", "header", "aside"]):
                element.decompose()
            
            # Extract title
            title = soup.find('title')
            title_text = title.get_text().strip() if title else "No title"
            
            # Extract main content (prioritize main, article, content areas)
            main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
            if main_content:
                content = main_content.get_text()
            else:
                content = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in content.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            clean_text = ' '.join(chunk for chunk in chunks if chunk)
            
            # Extract headings for structure
            headings = []
            for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                headings.append(tag.get_text().strip())
            
            # Truncate if too long
            if len(clean_text) > max_length:
                clean_text = clean_text[:max_length] + "..."
            
            return {
                'url': url,
                'title': title_text,
                'content': clean_text,
                'headings': headings[:10],  # First 10 headings
                'word_count': len(clean_text.split()),
                'success': True
            }
            
        except Exception as e:
            return {
                'url': url,
                'title': 'Error',
                'content': f"Error scraping {url}: {str(e)}",
                'headings': [],
                'word_count': 0,
                'success': False
            }

class SemanticRetriever(dspy.Module):
    """Advanced DSPy module for semantic information retrieval"""
    
    def __init__(self, reasoning_approach: str = "cot"):
        """
        Initialize with flexible reasoning approach
        
        Args:
            reasoning_approach: "cot" for ChainOfThought or "react" for ReAct
        """
        super().__init__()
        self.reasoning_approach = reasoning_approach.lower()
        
        if self.reasoning_approach == "react":
            self.retrieval_signature = dspy.Signature(
                "query, document_content, document_title -> thought, action, relevant_passages, key_points, relevance_score",
                "Given a research query and document content, think step by step, take action, extract the most relevant passages, identify key points, and score relevance"
            )
            self.retriever = dspy.ReAct(self.retrieval_signature)
        else:  # Default to ChainOfThought
            self.retrieval_signature = dspy.Signature(
                "query, document_content, document_title -> relevant_passages, key_points, relevance_score",
                "Given a research query and document content, extract the most relevant passages, identify key points, and score relevance"
            )
            self.retriever = dspy.ChainOfThought(self.retrieval_signature)
    
    def forward(self, query: str, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Retrieve and process information from multiple documents"""
        processed_docs = []
        
        for doc in documents:
            if not doc['success']:
                continue
                
            try:
                result = self.retriever(
                    query=query, 
                    document_content=doc['content'],
                    document_title=doc['title']
                )
                
                processed_docs.append({
                    'url': doc['url'],
                    'title': doc['title'],
                    'content': doc['content'],
                    'headings': doc['headings'],
                    'relevant_passages': result.relevant_passages,
                    'key_points': result.key_points,
                    'relevance_score': float(result.relevance_score) if hasattr(result, 'relevance_score') else 0.5,
                    'word_count': doc['word_count']
                })
            except Exception as e:
                # Fallback processing
                processed_docs.append({
                    'url': doc['url'],
                    'title': doc['title'],
                    'content': doc['content'],
                    'headings': doc['headings'],
                    'relevant_passages': doc['content'][:2000],
                    'key_points': doc['headings'][:5],
                    'relevance_score': 0.3,
                    'word_count': doc['word_count']
                })
        
        # Sort by relevance score
        processed_docs.sort(key=lambda x: x['relevance_score'], reverse=True)
        return processed_docs

class MultiStepAnswerer(dspy.Module):
    """Advanced DSPy module for multi-step research question answering"""
    
    def __init__(self, reasoning_approach: str = "cot"):
        """
        Initialize with flexible reasoning approach
        
        Args:
            reasoning_approach: "cot" for ChainOfThought or "react" for ReAct
        """
        super().__init__()
        self.reasoning_approach = reasoning_approach.lower()
        
        # Step 1: Analyze the question
        if self.reasoning_approach == "react":
            self.question_analyzer = dspy.ReAct(
                dspy.Signature(
                    "question -> thought, action, question_type, key_concepts, required_depth",
                    "Analyze a research question step by step, think and take action to understand its type, key concepts, and required depth of analysis"
                )
            )
        else:  # Default to ChainOfThought
            self.question_analyzer = dspy.ChainOfThought(
                dspy.Signature(
                    "question -> question_type, key_concepts, required_depth",
                    "Analyze a research question to understand its type, key concepts, and required depth of analysis"
                )
            )
        
        # Step 2: Synthesize information
        if self.reasoning_approach == "react":
            self.synthesizer = dspy.ReAct(
                dspy.Signature(
                    "question, research_context, question_analysis -> thought, action, synthesized_information",
                    "Synthesize information from multiple sources step by step, thinking and taking action based on question analysis"
                )
            )
            self.answer_generator = dspy.ReAct(
                dspy.Signature(
                    "question, synthesized_information, question_analysis -> thought, action, comprehensive_answer, key_findings, confidence_score",
                    "Generate a comprehensive answer step by step, thinking and taking action to provide key findings and confidence assessment"
                )
            )
        else:  # Default to ChainOfThought
            self.synthesizer = dspy.ChainOfThought(
                dspy.Signature(
                    "question, research_context, question_analysis -> synthesized_information",
                    "Synthesize information from multiple sources based on question analysis"
                )
            )
            self.answer_generator = dspy.ChainOfThought(
                dspy.Signature(
                    "question, synthesized_information, question_analysis -> comprehensive_answer, key_findings, confidence_score",
                    "Generate a comprehensive answer with key findings and confidence assessment"
                )
            )
    
    def forward(self, question: str, research_context: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate a comprehensive answer using multi-step reasoning"""
        
        # Step 1: Analyze the question
        question_analysis = self.question_analyzer(question=question)
        
        # Step 2: Prepare research context
        combined_context = ""
        for info in research_context:
            combined_context += f"\n--- Source: {info['title']} ({info['url']}) ---\n"
            combined_context += f"Relevance Score: {info['relevance_score']:.2f}\n"
            combined_context += f"Key Points: {', '.join(info['key_points'])}\n"
            combined_context += f"Content: {info['relevant_passages']}\n"
            combined_context += "\n"
        
        # Step 3: Synthesize information
        synthesis = self.synthesizer(
            question=question,
            research_context=combined_context,
            question_analysis=question_analysis
        )
        
        # Step 4: Generate final answer
        final_result = self.answer_generator(
            question=question,
            synthesized_information=synthesis.synthesized_information,
            question_analysis=question_analysis
        )
        
        return {
            'answer': final_result.comprehensive_answer,
            'key_findings': final_result.key_findings.split('\n') if hasattr(final_result, 'key_findings') else [],
            'confidence_score': float(final_result.confidence_score) if hasattr(final_result, 'confidence_score') else 0.7,
            'question_analysis': question_analysis
        }

class OptimizedResearchSystem:
    """Advanced research system with optimization capabilities"""
    
    def __init__(self, reasoning_approach: str = "cot"):
        """
        Initialize the optimized research system with flexible reasoning approach
        
        Args:
            reasoning_approach: "cot" for ChainOfThought or "react" for ReAct
        """
        self.reasoning_approach = reasoning_approach.lower()
        self.scraper = AdvancedWebScraper()
        self.retriever = SemanticRetriever(reasoning_approach=self.reasoning_approach)
        self.answerer = MultiStepAnswerer(reasoning_approach=self.reasoning_approach)
    
    def research(self, question: str, urls: List[str], max_sources: int = 5) -> ResearchResult:
        """Conduct optimized deep research on a question"""
        
        print(f"🔍 Researching: {question}")
        print(f"📚 Sources: {len(urls)} URLs")
        
        # Step 1: Scrape and process all URLs
        print("\n📖 Scraping and processing sources...")
        documents = []
        for url in urls:
            doc = self.scraper.extract_text_from_url(url)
            documents.append(doc)
            if doc['success']:
                print(f"  ✅ {doc['title']} ({doc['word_count']} words)")
            else:
                print(f"  ❌ Failed to scrape {url}")
        
        # Step 2: Retrieve relevant information
        print("\n🔍 Analyzing content for relevance...")
        research_context = self.retriever(question, documents)
        
        # Filter to top sources
        research_context = research_context[:max_sources]
        
        print(f"📊 Using top {len(research_context)} most relevant sources:")
        for i, info in enumerate(research_context, 1):
            print(f"  {i}. {info['title']} (relevance: {info['relevance_score']:.2f})")
        
        # Step 3: Generate comprehensive answer
        print("\n🤔 Synthesizing information and generating answer...")
        answer_data = self.answerer(question, research_context)
        
        return ResearchResult(
            question=question,
            answer=answer_data['answer'],
            sources_used=[info['url'] for info in research_context],
            confidence_score=answer_data['confidence_score'],
            key_findings=answer_data['key_findings'],
            research_context=research_context
        )
    
    def research_with_follow_up(self, question: str, urls: List[str]) -> ResearchResult:
        """Conduct research with automatic follow-up question generation"""
        
        # Initial research
        result = self.research(question, urls)
        
        # Generate follow-up questions
        follow_up_signature = dspy.Signature(
            "original_question, research_answer -> follow_up_questions",
            "Generate 2-3 follow-up questions to deepen the research"
        )
        follow_up_generator = dspy.ChainOfThought(follow_up_signature)
        
        try:
            follow_up_result = follow_up_generator(
                original_question=question,
                research_answer=result.answer
            )
            print(f"\n💡 Suggested follow-up questions:")
            follow_up_questions = follow_up_result.follow_up_questions.split('\n')
            for i, q in enumerate(follow_up_questions[:3], 1):
                if q.strip():
                    print(f"  {i}. {q.strip()}")
        except Exception as e:
            print(f"\n⚠️  Could not generate follow-up questions: {e}")
        
        return result

# Example usage and testing
if __name__ == "__main__":
    # Initialize the advanced research system
    research_system = OptimizedResearchSystem()
    
    # Example research questions
    questions = [
        "What are the key principles and benefits of using DSPy for AI programming?",
        "How does DSPy's optimization approach differ from traditional prompt engineering?",
        "What are the main modules and components available in DSPy?"
    ]
    
    # URLs to research
    urls = [
        "https://dspy.ai/",
        "https://github.com/stanfordnlp/dspy",
        "https://dspy.ai/tutorials/",
        "https://dspy.ai/docs/",
        "https://dspy.ai/docs/programming/"
    ]
    
    # Test with the first question
    question = questions[0]
    result = research_system.research_with_follow_up(question, urls)
    
    print("\n" + "="*100)
    print("ADVANCED RESEARCH RESULTS")
    print("="*100)
    print(f"\nQuestion: {result.question}")
    print(f"\nConfidence Score: {result.confidence_score:.2f}")
    print(f"\nAnswer:\n{result.answer}")
    
    if result.key_findings:
        print(f"\nKey Findings:")
        for i, finding in enumerate(result.key_findings, 1):
            if finding.strip():
                print(f"  {i}. {finding.strip()}")
    
    print(f"\nSources used: {len(result.sources_used)}")
    for i, url in enumerate(result.sources_used, 1):
        print(f"  {i}. {url}")
