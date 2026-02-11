"""
Enrichment Node - Enriches news with detailed content and stores in VectorDB
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from src.tools.websearch.duckduckgo_agent import DuckDuckGoAgent
from src.rag.vectordb import VectorDB


def enrichment_node(state):
    """
    Enrich news items with detailed content and store in VectorDB
    
    Args:
        state: Pipeline state with 'news_items'
    
    Returns:
        Updated state with enrichment complete
    """
    print("\n" + "="*50)
    print("🔍 ENRICHMENT NODE - Getting detailed content...")
    print("="*50)
    
    news_items = state.get("news_items", [])
    
    if not news_items:
        print("⚠️ No news items to enrich")
        return state
    
    try:
        # Initialize agents
        ddg_agent = DuckDuckGoAgent()
        vectordb = VectorDB()
        
        # Enrich each news item
        enriched_items = []
        
        for i, item in enumerate(news_items):
            print(f"  Enriching {i+1}/{len(news_items)}...", end="\r")
            
            # Get detailed content from DuckDuckGo
            detailed_content = ddg_agent.enrich_news(item["headline"])
            
            # Combine headline + enriched content
            full_content = f"{item['headline']}\n\n{detailed_content}" if detailed_content else item["headline"]
            
            enriched_items.append({
                "id": i,
                "headline": item["headline"],
                "content": full_content,
                "source": item.get("source", "unknown"),
                "sentiment": item.get("sentiment", "neutral")
            })
        
        # Store in VectorDB
        print(f"\n💾 Storing in VectorDB...")
        vectordb.add_documents(enriched_items)
        
        print(f"✅ Enriched and stored {len(enriched_items)} items")
        
        state["enrichment_complete"] = True
        return state
    
    except Exception as e:
        print(f"⚠️ Enrichment error: {e}")
        state["enrichment_complete"] = False
        return state


# Test
if __name__ == "__main__":
    state = {
        "news_items": [
            {"headline": "India wins Test series against Australia", "source": "espn", "sentiment": "positive"},
            {"headline": "Virat Kohli scores century", "source": "reddit", "sentiment": "positive"}
        ]
    }
    
    state = enrichment_node(state)
    print(f"\nEnrichment complete: {state.get('enrichment_complete')}")