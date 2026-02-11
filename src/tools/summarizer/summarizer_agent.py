"""
Summarizer Agent - Generates summaries using Groq LLM
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from groq import Groq
from src.config.settings import GROQ_API_KEY


class SummarizerAgent:
    """Generates summaries using Groq LLM"""
    
    def __init__(self):
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY not configured")
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = "llama-3.3-70b-versatile"
    
    def summarize(self, headline, content=""):
        """
        Generate a short summary for a news item
        
        Args:
            headline: News headline
            content: Additional content/context (optional)
        
        Returns:
            Summary string (1-2 lines)
        """
        try:
            text = headline
            if content:
                text = f"{headline}\n\nDetails: {content}"
            
            prompt = f"""Summarize this cricket news in 1-2 short sentences:

{text}

Summary:"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=100
            )
            
            summary = response.choices[0].message.content.strip()
            return summary
        
        except Exception as e:
            print(f"⚠️ Summarizer error: {e}")
            return headline  # Fallback to headline
    
    def generate_executive_summary(self, news_items):
        """
        Generate overall summary of all news
        
        Args:
            news_items: List of news dictionaries with 'headline' key
        
        Returns:
            Executive summary string (3-4 lines)
        """
        try:
            # Prepare headlines list
            headlines = "\n".join([f"- {item['headline']}" for item in news_items[:15]])
            
            prompt = f"""Here are today's cricket news headlines:

{headlines}

Write a brief executive summary (3-4 sentences) highlighting the main themes and most important news:"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=200
            )
            
            summary = response.choices[0].message.content.strip()
            return summary
        
        except Exception as e:
            print(f"⚠️ Executive summary error: {e}")
            return "Today's cricket news covers various updates from around the world."


# Test
if __name__ == "__main__":
    agent = SummarizerAgent()
    
    # Test single summary
    headline = "Virat Kohli scores his 81st international century against Australia in Sydney Test"
    summary = agent.summarize(headline)
    print(f"Headline: {headline}")
    print(f"Summary: {summary}")
    
    print("\n" + "="*50 + "\n")
    
    # Test executive summary
    news = [
        {"headline": "India wins Test series against Australia 3-1"},
        {"headline": "Kohli scores century in final Test"},
        {"headline": "Bumrah takes 5 wickets in first innings"}
    ]
    exec_summary = agent.generate_executive_summary(news)
    print(f"Executive Summary:\n{exec_summary}")