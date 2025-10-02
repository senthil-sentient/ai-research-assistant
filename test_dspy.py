import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import List, Dict, Any
import re

# Configure DSPy for serverless deployment
from dspy_config import get_dspy_lm
import dspy

# Configure DSPy
lm = get_dspy_lm()

class WebScraper:
    """Utility class for scraping and processing web content"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def extract_text_from_url(self, url: str, max_length: int = 10000) -> str:
        """Extract clean text content from a URL"""
        print("Call to Scraping--------------------------------")
        print(url)
        print("End of Call to Scraping--------------------------------")
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            # Truncate if too long
            if len(text) > max_length:
                text = text[:max_length] + "..."
                
            return text
            
        except Exception as e:
            return f"Error scraping {url}: {str(e)}"
    
    def extract_links_from_url(self, url: str, max_links: int = 5) -> List[str]:
        """Extract relevant links from a webpage"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            base_url = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
            
            links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(base_url, href)
                
                # Filter for relevant links (same domain, not external)
                if urlparse(full_url).netloc == urlparse(url).netloc:
                    links.append(full_url)
                    
                if len(links) >= max_links:
                    break
                    
            return links
            
        except Exception as e:
            return []

class ResearchRetriever(dspy.Module):
    """DSPy module for retrieving and processing research information"""
    
    def __init__(self, reasoning_approach: str = "cot"):
        """
        Initialize with flexible reasoning approach
        
        Args:
            reasoning_approach: "cot" for ChainOfThought or "react" for ReAct
        """
        super().__init__()
        self.scraper = WebScraper()
        self.reasoning_approach = reasoning_approach.lower()
        
        if self.reasoning_approach == "react":
            self.retrieval_signature = dspy.Signature(
                "query, available_urls -> thought, action, relevant_passages",
                "Given a research query and available URLs, think step by step about which URLs to explore, take action to extract content from relevant URLs (use extract_text_tool), and provide the most relevant passages. Stop when you have sufficient information to answer the query."
            )
            # Create a tool wrapper for the scraper method
            def extract_text_tool(url: str) -> str:
                """Tool to extract text content from a URL"""
                return self.scraper.extract_text_from_url(url)
            
            self.retriever = dspy.ReAct(self.retrieval_signature, tools=[extract_text_tool])
        else:  # Default to ChainOfThought
            self.retrieval_signature = dspy.Signature(
                "query, context -> relevant_passages",
                "Given a research query and context, extract the most relevant passages"
            )
            self.retriever = dspy.ChainOfThought(self.retrieval_signature)
    
    def forward(self, query: str, urls: List[str]) -> List[Dict[str, str]]:
        """Retrieve and process information from multiple URLs"""
        retrieved_info = []
        
        if self.reasoning_approach == "react":
            # For ReAct: Let it decide which URLs to explore using tools
            try:
                # Format available URLs for ReAct to choose from
                available_urls = "\n".join([f"- {url}" for url in urls])
                
                print(f"🔍 ReAct analyzing query and available URLs:")
                print(f"Query: {query}")
                print(f"Available URLs: {urls}")
                print("ReAct will now decide which URLs to explore...")
                
                # Let ReAct make its own decisions about which URLs to scrape
                result = self.retriever(query=query, available_urls=available_urls)
                
                print("--------------------------------")
                print("ReAct Decision Process:")
                print(f"Thought: {getattr(result, 'thought', 'N/A')}")
                print(f"Action: {getattr(result, 'action', 'N/A')}")
                print(f"Relevant Passages: {result.relevant_passages[:300]}...")
                print("--------------------------------")
                
                # ReAct should have used the tool to explore URLs and extract content
                retrieved_info.append({
                    'urls_available': urls,
                    'relevant_passages': result.relevant_passages,
                    'thought': getattr(result, 'thought', ''),
                    'action': getattr(result, 'action', ''),
                    'reasoning_approach': self.reasoning_approach
                })
                
            except Exception as e:
                print(f"ReAct processing failed: {e}")
                # Fallback: process URLs manually if ReAct fails
                print("Falling back to manual URL processing...")
                for url in urls:
                    content = self.scraper.extract_text_from_url(url)
                    if not content.startswith("Error"):
                        retrieved_info.append({
                            'url': url,
                            'content': content,
                            'relevant_passages': content[:2000],
                            'reasoning_approach': self.reasoning_approach
                        })
        else:
            # For ChainOfThought: Process URLs sequentially as before
            for url in urls:
                # Extract text content
                content = self.scraper.extract_text_from_url(url)
                
                if content.startswith("Error"):
                    continue
                    
                # Use DSPy to extract relevant passages
                try:
                    result = self.retriever(query=query, context=content)
                    
                    # Handle different output formats based on reasoning approach
                    relevant_passages = result.relevant_passages
                    
                    retrieved_info.append({
                        'url': url,
                        'content': content,
                        'relevant_passages': relevant_passages,
                        'reasoning_approach': self.reasoning_approach
                    })
                except Exception as e:
                    # Fallback to using the full content if DSPy processing fails
                    retrieved_info.append({
                        'url': url,
                        'content': content,
                        'relevant_passages': content[:2000],  # First 2000 chars as fallback
                        'reasoning_approach': self.reasoning_approach
                    })
        
        return retrieved_info

class ResearchAnswerer(dspy.Module):
    """DSPy module for answering research questions based on retrieved information"""
    
    def __init__(self, reasoning_approach: str = "cot"):
        """
        Initialize with flexible reasoning approach
        
        Args:
            reasoning_approach: "cot" for ChainOfThought or "react" for ReAct
        """
        super().__init__()
        self.reasoning_approach = reasoning_approach.lower()
        
        if self.reasoning_approach == "react":
            self.answer_signature = dspy.Signature(
                "question, research_context -> thought, answer",
                "Given a research question and context from multiple sources, think step by step, and provide a comprehensive answer"
            )
            # Create a simple tool for the answerer (can be empty or have basic tools)
            def analyze_context_tool(context: str) -> str:
                """Tool to analyze research context"""
                return f"Analyzed context with {len(context)} characters"
            
            self.answerer = dspy.ReAct(self.answer_signature, tools=[analyze_context_tool])
        else:  # Default to ChainOfThought
            self.answer_signature = dspy.Signature(
                "question, research_context -> answer",
                "Given a research question and context from multiple sources, provide a comprehensive answer"
            )
            self.answerer = dspy.ChainOfThought(self.answer_signature)
    
    def forward(self, question: str, research_context: List[Dict[str, str]]) -> Dict[str, Any]:
        """Generate a comprehensive answer based on research context"""
        
        # Combine all relevant passages
        combined_context = ""
        for info in research_context:
            # Handle different data structures from different reasoning approaches
            if 'url' in info:
                # ChainOfThought structure
                combined_context += f"\n--- Source: {info['url']} ---\n"
            elif 'urls_available' in info:
                # ReAct structure
                combined_context += f"\n--- Sources: {', '.join(info['urls_available'])} ---\n"
            else:
                # Fallback
                combined_context += f"\n--- Source: Unknown ---\n"
            
            combined_context += info['relevant_passages']
            combined_context += "\n"
        
        # Generate answer using DSPy
        result = self.answerer(question=question, research_context=combined_context)
        
        # Handle different output formats based on reasoning approach
        if self.reasoning_approach == "react":
            return {
                'answer': result.answer,
                'thought': result.thought if hasattr(result, 'thought') else None,
                'action': result.action if hasattr(result, 'action') else None,
                'reasoning_approach': self.reasoning_approach
            }
        else:  # ChainOfThought
            return {
                'answer': result.answer,
                'reasoning_approach': self.reasoning_approach
            }

class DeepResearchSystem:
    """Main system for conducting deep research using DSPy"""
    
    def __init__(self, reasoning_approach: str = "cot"):
        """
        Initialize the research system with flexible reasoning approach
        
        Args:
            reasoning_approach: "cot" for ChainOfThought or "react" for ReAct
        """
        self.reasoning_approach = reasoning_approach.lower()
        self.retriever = ResearchRetriever(reasoning_approach=self.reasoning_approach)
        self.answerer = ResearchAnswerer(reasoning_approach=self.reasoning_approach)
        self.scraper = WebScraper()
    
    def research(self, question: str, urls: List[str]) -> Dict[str, Any]:
        """Conduct deep research on a question using multiple sources"""
        
        print(f"🔍 Researching: {question}")
        print(f"📚 Sources: {len(urls)} URLs")
        print(f"🧠 Reasoning approach: {self.reasoning_approach.upper()}")
        
        # Step 1: Retrieve relevant information
        print("\n📖 Retrieving information from sources...")
        research_context = self.retriever(question, urls)
        
        # Step 2: Generate comprehensive answer
        print("🤔 Analyzing and synthesizing information...")
        answer_result = self.answerer(question, research_context)
        
        # Extract sources used based on data structure
        sources_used = []
        for info in research_context:
            if 'url' in info:
                sources_used.append(info['url'])
            elif 'urls_available' in info:
                sources_used.extend(info['urls_available'])
        
        return {
            'question': question,
            'answer': answer_result['answer'],
            'reasoning_approach': self.reasoning_approach,
            'sources_used': sources_used,
            'research_context': research_context,
            'additional_info': answer_result  # Contains thought/action for ReAct
        }

# Example usage
if __name__ == "__main__":
    # Example research question
    question = "What does Banyan do?"
    
    # URLs to research
    urls = [
        "https://www.icicibank.com/personal-banking/accounts/salary-account",
        "https://www.icicibank.com/personal-banking/accounts/salary-account"
    ]
    
    # Test both reasoning approaches
    print("="*80)
    print("TESTING DIFFERENT REASONING APPROACHES")
    print("="*80)
    
    # Test ChainOfThought approach
    print("\n🧠 Testing ChainOfThought approach...")
    cot_system = DeepResearchSystem(reasoning_approach="cot")
    cot_result = cot_system.research(question, urls)
    
    print("\n" + "="*80)
    print("CHAIN OF THOUGHT RESULTS")
    print("="*80)
    print(f"\nQuestion: {cot_result['question']}")
    print(f"\nAnswer:\n{cot_result['answer']}")
    print(f"\nSources used: {len(cot_result['sources_used'])}")
    
    # Test ReAct approach
    print("\n🧠 Testing ReAct approach...")
    react_system = DeepResearchSystem(reasoning_approach="react")
    react_result = react_system.research(question, urls)
    
    print("\n" + "="*80)
    print("REACT RESULTS")
    print("="*80)
    print(f"\nQuestion: {react_result['question']}")
    print(f"\nAnswer:\n{react_result['answer']}")
    if react_result['additional_info'].get('thought'):
        print(f"\nThought process:\n{react_result['additional_info']['thought']}")
    if react_result['additional_info'].get('action'):
        print(f"\nActions taken:\n{react_result['additional_info']['action']}")
    print(f"\nSources used: {len(react_result['sources_used'])}")