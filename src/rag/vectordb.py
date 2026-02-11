"""
VectorDB - Stores and retrieves news embeddings using ChromaDB
"""

import chromadb
from chromadb.config import Settings
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.config.settings import VECTORDB_PATH


class VectorDB:
    """ChromaDB wrapper for storing news embeddings"""
    
    def __init__(self):
        # Ensure directory exists
        os.makedirs(VECTORDB_PATH, exist_ok=True)
        
        # Initialize ChromaDB with persistent storage
        self.client = chromadb.PersistentClient(path=VECTORDB_PATH)
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="cricket_news",
            metadata={"description": "Cricket news for RAG"}
        )
    
    def add_documents(self, news_items):
        """
        Add news items to vector database
        
        Args:
            news_items: List of dicts with 'id', 'headline', 'content'
        
        Returns:
            Number of documents added
        """
        if not news_items:
            return 0
        
        try:
            ids = []
            documents = []
            metadatas = []
            
            for item in news_items:
                # Create unique ID
                doc_id = f"news_{item.get('id', '')}_{hash(item['headline']) % 10000}"
                
                ids.append(doc_id)
                documents.append(item.get("content", item["headline"]))
                metadatas.append({
                    "headline": item["headline"][:200],
                    "source": item.get("source", "unknown")
                })
            
            # Add to collection (ChromaDB handles embeddings automatically)
            self.collection.add(
                ids=ids,
                documents=documents,
                metadatas=metadatas
            )
            
            return len(ids)
        
        except Exception as e:
            print(f"⚠️ VectorDB add error: {e}")
            return 0
    
    def search(self, query, n_results=5):
        """
        Search for relevant documents
        
        Args:
            query: Search query
            n_results: Number of results to return
        
        Returns:
            List of relevant documents with metadata
        """
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            # Format results
            documents = []
            
            if results and results["documents"]:
                for i, doc in enumerate(results["documents"][0]):
                    metadata = results["metadatas"][0][i] if results["metadatas"] else {}
                    distance = results["distances"][0][i] if results["distances"] else 0
                    
                    documents.append({
                        "content": doc,
                        "headline": metadata.get("headline", ""),
                        "source": metadata.get("source", "unknown"),
                        "relevance": round(1 - distance, 2)  # Convert distance to relevance
                    })
            
            return documents
        
        except Exception as e:
            print(f"⚠️ VectorDB search error: {e}")
            return []
    
    def get_count(self):
        """Get total number of documents in collection"""
        try:
            return self.collection.count()
        except:
            return 0
    
    def clear(self):
        """Clear all documents from collection"""
        try:
            self.client.delete_collection("cricket_news")
            self.collection = self.client.get_or_create_collection(
                name="cricket_news",
                metadata={"description": "Cricket news for RAG"}
            )
            return True
        except Exception as e:
            print(f"⚠️ VectorDB clear error: {e}")
            return False


# Test
if __name__ == "__main__":
    db = VectorDB()
    
    # Test adding documents
    test_items = [
        {
            "id": 1,
            "headline": "India wins Test series against Australia",
            "content": "India wins Test series against Australia. Virat Kohli scored a brilliant century in the final test match held in Sydney.",
            "source": "espn"
        },
        {
            "id": 2,
            "headline": "Bumrah takes 5 wickets",
            "content": "Jasprit Bumrah takes 5 wickets in the first innings. His yorkers were unplayable.",
            "source": "reddit"
        }
    ]
    
    added = db.add_documents(test_items)
    print(f"Added {added} documents")
    print(f"Total documents: {db.get_count()}")
    
    # Test search
    print("\nSearching for 'Kohli century'...")
    results = db.search("Kohli century", n_results=2)
    for r in results:
        print(f"  - {r['headline'][:50]}... (relevance: {r['relevance']})")