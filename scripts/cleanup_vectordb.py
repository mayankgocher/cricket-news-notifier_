"""
Cleanup VectorDB - Remove old embeddings
Run manually: python scripts/cleanup_vectordb.py --days 90
"""

import sys
import os
import argparse
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.rag.vectordb import VectorDB


def cleanup_vectordb(days_to_keep=90):
    """
    Clear VectorDB completely (ChromaDB doesn't support date-based deletion easily)
    For simplicity, we clear all and let it rebuild from next pipeline run
    
    Args:
        days_to_keep: Not used currently, but kept for API consistency
    """
    print("\n" + "="*50)
    print("🗑️  VectorDB Cleanup")
    print("="*50)
    
    try:
        db = VectorDB()
        
        # Get count before
        count_before = db.get_count()
        print(f"📊 Documents before: {count_before}")
        
        # Clear all
        success = db.clear()
        
        if success:
            count_after = db.get_count()
            print(f"📊 Documents after: {count_after}")
            print(f"\n✅ VectorDB cleared successfully!")
            print(f"   Deleted {count_before} documents")
            print("\n💡 Note: VectorDB will be repopulated on next pipeline run")
        else:
            print("❌ Failed to clear VectorDB")
    
    except Exception as e:
        print(f"❌ Cleanup error: {e}")
    
    print("="*50 + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cleanup VectorDB")
    parser.add_argument(
        "--days",
        type=int,
        default=90,
        help="Days to keep (note: currently clears all, for rebuild)"
    )
    
    args = parser.parse_args()
    
    # Confirmation
    print("⚠️  Warning: This will clear ALL documents from VectorDB")
    print("   The database will be repopulated on next pipeline run")
    confirm = input("Continue? (yes/no): ")
    
    if confirm.lower() == "yes":
        cleanup_vectordb(args.days)
    else:
        print("Cleanup cancelled")