"""
RSS Agent - Fetches cricket news from ESPN Cricinfo and other RSS feeds
"""

import feedparser
from datetime import datetime
import time


class RSSAgent:
    """Fetches cricket news from RSS feeds"""
    
    def __init__(self):
        # Cricket RSS feed URLs
        self.feeds = {
            "espn": "https://www.espncricinfo.com/rss/content/story/feeds/0.xml",
            "icc": "https://www.icc-cricket.com/news/rss",
            "cricbuzz": "https://www.cricbuzz.com/rss/cricket-news",
            "ndtv_cricket": "https://feeds.feedburner.com/ndtvcricketnews",
            "guardian_cricket": "https://www.theguardian.com/sport/cricket/rss",
            "bbc_cricket": "http://feeds.bbci.co.uk/sport/cricket/rss.xml"
        }
    
    def fetch_news(self, limit=20):
        """
        Fetch cricket news from RSS feeds
        
        Args:
            limit: Number of news items to return
        
        Returns:
            List of news dictionaries
        """
        print(f"📥 Fetching RSS feeds...")
        
        all_news = []
        
        for source, url in self.feeds.items():
            try:
                feed = feedparser.parse(url)
                
                for entry in feed.entries[:10]:  # Max 10 per source
                    # Parse publish date
                    timestamp = None
                    if hasattr(entry, "published_parsed") and entry.published_parsed:
                        timestamp = time.mktime(entry.published_parsed)
                    
                    # Get summary if available
                    summary = ""
                    if hasattr(entry, "summary"):
                        summary = entry.summary[:500]  # Limit summary length
                    
                    all_news.append({
                        "headline": entry.title,
                        "summary": summary,
                        "source": source,
                        "url": entry.link,
                        "timestamp": timestamp
                    })
                
                print(f"  ✓ {source}: {len(feed.entries[:10])} items")
            
            except Exception as e:
                print(f"  ✗ {source}: Error - {e}")
                continue
        
        # Sort by timestamp (newest first)
        all_news.sort(key=lambda x: x.get("timestamp") or 0, reverse=True)
        
        # Return limited results
        result = all_news[:limit]
        print(f"✅ Fetched {len(result)} RSS items total")
        return result


# Test
if __name__ == "__main__":
    agent = RSSAgent()
    news = agent.fetch_news(limit=5)
    for item in news:
        print(f"- [{item['source']}] {item['headline'][:50]}...")