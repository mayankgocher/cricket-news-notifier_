"""
Newsletter Node - Prepares newsletter content with summaries
"""

import sys
import os
from datetime import datetime
import pytz

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from src.tools.summarizer.summarizer_agent import SummarizerAgent
from src.config.settings import TIMEZONE


def newsletter_node(state):
    """
    Prepare newsletter content with executive summary and item summaries
    
    Args:
        state: Pipeline state with 'news_items'
    
    Returns:
        Updated state with 'newsletter_content'
    """
    print("\n" + "="*50)
    print("📰 NEWSLETTER NODE - Preparing content...")
    print("="*50)
    
    news_items = state.get("news_items", [])
    
    if not news_items:
        print("⚠️ No news items for newsletter")
        state["newsletter_content"] = "No cricket news available today."
        return state
    
    try:
        # Initialize summarizer
        summarizer = SummarizerAgent()
        
        # Generate executive summary
        executive_summary = summarizer.generate_executive_summary(news_items)
        
        # Generate individual summaries for each item
        print("  Generating summaries...")
        for i, item in enumerate(news_items):
            print(f"    Summarizing {i+1}/{len(news_items)}...", end="\r")
            
            # Use enriched content if available, otherwise headline
            content = item.get("enriched_content", "") or item.get("summary", "") or item["headline"]
            
            # Generate short summary (1-2 lines)
            item["short_summary"] = summarizer.summarize(item["headline"], content)
        
        print(f"    Summarized {len(news_items)} items.     ")
        
        # Get current date in IST
        tz = pytz.timezone(TIMEZONE)
        today = datetime.now(tz).strftime("%B %d, %Y")
        
        # Build newsletter content
        content = f"""
🏏 CRICKET DAILY DIGEST - {today}
{'='*45}

📋 EXECUTIVE SUMMARY
{executive_summary}

{'='*45}
📰 TODAY'S NEWS
{'='*45}

"""
        # Add each news item with summary
        for i, item in enumerate(news_items, 1):
            # Sentiment emoji
            emoji = {
                "positive": "🟢",
                "negative": "🔴",
                "neutral": "🟡"
            }.get(item.get("sentiment", "neutral"), "🟡")
            
            # Source badge
            source = item.get("source", "unknown").upper()
            
            # Get summary
            summary = item.get("short_summary", "")
            
            # Format item with summary
            content += f"{i}. {emoji} {item['headline']}\n"
            if summary and summary != item['headline']:
                content += f"   📝 {summary}\n"
            content += f"   [{source}]\n\n"
        
        # Import frontend URL
        from src.config.settings import FRONTEND_URL
        
        # Footer with links
        content += f"""
{'='*45}

💬 Want more details?
   → Ask questions: {FRONTEND_URL}

🔕 Unsubscribe:
   → Email users: {FRONTEND_URL} (go to Subscribe page)
   → Telegram users: Send /unsubscribe

{'='*45}
"""
        
        print(f"✅ Newsletter prepared with {len(news_items)} items")
        
        state["newsletter_content"] = content
        state["executive_summary"] = executive_summary
        return state
    
    except Exception as e:
        print(f"⚠️ Newsletter error: {e}")
        state["newsletter_content"] = "Error preparing newsletter."
        return state


# Test
if __name__ == "__main__":
    state = {
        "news_items": [
            {"headline": "India wins Test series against Australia", "source": "espn", "sentiment": "positive", "enriched_content": "India won the Border-Gavaskar Trophy 3-1. Virat Kohli scored two centuries."},
            {"headline": "Kohli scores century in final Test", "source": "reddit", "sentiment": "positive", "enriched_content": "Virat Kohli hit his 30th Test century to help India win."},
            {"headline": "Bumrah ruled out with injury", "source": "twitter", "sentiment": "negative", "enriched_content": "Jasprit Bumrah will miss 3 months due to back stress fracture."}
        ]
    }
    
    state = newsletter_node(state)
    print(state["newsletter_content"])