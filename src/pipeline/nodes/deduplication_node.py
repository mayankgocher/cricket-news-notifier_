"""
Deduplication Node - Removes duplicate news using LLM
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from groq import Groq
from src.config.settings import GROQ_API_KEY
import json


def deduplication_node(state):
    """
    Remove duplicate news items using LLM
    
    Args:
        state: Pipeline state with 'news_items'
    
    Returns:
        Updated state with deduplicated news
    """
    print("\n" + "="*50)
    print("🔄 DEDUPLICATION NODE - Removing duplicates...")
    print("="*50)
    
    news_items = state.get("news_items", [])
    
    if len(news_items) <= 5:
        print("✅ Too few items, skipping deduplication")
        return state
    
    try:
        client = Groq(api_key=GROQ_API_KEY)
        
        # Prepare headlines with indices
        headlines_text = ""
        for i, item in enumerate(news_items):
            headlines_text += f"{i}. {item['headline'][:100]}\n"
        
        prompt = f"""Here are {len(news_items)} cricket news headlines. Some may be about the same story.

{headlines_text}

Task: Identify duplicate/similar stories and return ONLY the index numbers to KEEP (one per story).
Return as JSON array of indices, e.g., [0, 2, 5, 7, 10]

Keep the headline with more detail or from better source (ESPN > Reddit > Twitter).
Return ONLY the JSON array, nothing else."""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=500
        )
        
        result = response.choices[0].message.content.strip()
        
        # Parse indices from response
        # Clean up response - extract JSON array
        if "[" in result and "]" in result:
            start = result.index("[")
            end = result.rindex("]") + 1
            result = result[start:end]
        
        keep_indices = json.loads(result)
        
        # Filter news items
        deduplicated = []
        for i in keep_indices:
            if 0 <= i < len(news_items):
                deduplicated.append(news_items[i])
        
        print(f"✅ Reduced {len(news_items)} → {len(deduplicated)} items")
        
        state["news_items"] = deduplicated
        return state
    
    except Exception as e:
        print(f"⚠️ Deduplication error: {e}")
        print("   Keeping all items...")
        return state


# Test
if __name__ == "__main__":
    # Test with sample data
    state = {
        "news_items": [
            {"headline": "Kohli scores century against Australia", "source": "espn"},
            {"headline": "KOHLI 100! What an innings vs AUS", "source": "twitter"},
            {"headline": "Bumrah takes 5 wickets in first innings", "source": "reddit"},
            {"headline": "India's Bumrah gets fifer against England", "source": "espn"},
            {"headline": "IPL 2025 auction date announced", "source": "reddit"}
        ]
    }
    
    state = deduplication_node(state)
    print(f"\nKept items:")
    for item in state["news_items"]:
        print(f"  - [{item['source']}] {item['headline'][:50]}...")