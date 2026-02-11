"""
Query Engine - Answers user questions using RAG
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.rag.vectordb import VectorDB
from src.config.settings import GROQ_API_KEY
from groq import Groq


class QueryEngine:
    """Answers questions using RAG (Retrieval Augmented Generation)"""
    
    def __init__(self):
        self.vectordb = VectorDB()
        self.llm = Groq(api_key=GROQ_API_KEY)
        self.model = "llama-3.1-8b-instant"
    
    def answer(self, question):
        """
        Answer a question using RAG
        
        Args:
            question: User's question
        
        Returns:
            Answer string
        """
        try:
            # Step 1: Search VectorDB for relevant content
            relevant_docs = self.vectordb.search(question, n_results=3)
            
            if not relevant_docs:
                return "I don't have enough information to answer that question. Please try asking about recent cricket news."
            
            # Step 2: Build context from retrieved documents
            context = ""
            for i, doc in enumerate(relevant_docs, 1):
                context += f"\n[Source {i}: {doc['source'].upper()}]\n"
                context += f"{doc['content']}\n"
            
            # Step 3: Generate answer using LLM
            prompt = f"""You are a cricket news assistant. Answer the user's question based on the provided news context.

CONTEXT:
{context}

USER QUESTION: {question}

Instructions:
- Answer based only on the provided context
- Be concise (2-4 sentences)
- If context doesn't contain the answer, say so
- Mention the source if relevant

ANSWER:"""

            response = self.llm.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=200
            )
            
            answer = response.choices[0].message.content.strip()
            return answer
        
        except Exception as e:
            print(f"⚠️ Query engine error: {e}")
            return "Sorry, I encountered an error while processing your question. Please try again."
    
    def answer_with_sources(self, question):
        """
        Answer question and return sources used
        
        Args:
            question: User's question
        
        Returns:
            Dict with 'answer' and 'sources'
        """
        try:
            # Search VectorDB
            relevant_docs = self.vectordb.search(question, n_results=3)
            
            if not relevant_docs:
                return {
                    "answer": "I don't have enough information to answer that question.",
                    "sources": []
                }
            
            # Build context
            context = ""
            sources = []
            
            for i, doc in enumerate(relevant_docs, 1):
                context += f"\n[{i}] {doc['content']}\n"
                sources.append({
                    "headline": doc["headline"],
                    "source": doc["source"],
                    "relevance": doc["relevance"]
                })
            
            # Generate answer
            prompt = f"""Answer this cricket question based on the context below.

CONTEXT:
{context}

QUESTION: {question}

Give a concise answer (2-4 sentences). Only use information from the context."""

            response = self.llm.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=200
            )
            
            answer = response.choices[0].message.content.strip()
            
            return {
                "answer": answer,
                "sources": sources
            }
        
        except Exception as e:
            print(f"⚠️ Query engine error: {e}")
            return {
                "answer": "Sorry, an error occurred. Please try again.",
                "sources": []
            }


# Test
if __name__ == "__main__":
    # First, add some test data to VectorDB
    db = VectorDB()
    
    test_items = [
        {
            "id": 1,
            "headline": "India wins Test series against Australia 3-1",
            "content": "India wins Test series against Australia 3-1. Virat Kohli was the star performer with two centuries. The final test in Sydney was drawn but India had already sealed the series.",
            "source": "espn"
        },
        {
            "id": 2,
            "headline": "Bumrah named Player of the Series",
            "content": "Jasprit Bumrah named Player of the Series for his 21 wickets. His yorkers and bouncers troubled the Australian batsmen throughout the series.",
            "source": "reddit"
        },
        {
            "id": 3,
            "headline": "IPL 2025 auction scheduled for December",
            "content": "IPL 2025 mega auction scheduled for December 15-16 in Jeddah. All teams will have new purse of 100 crores. Retention rules have been announced.",
            "source": "twitter"
        }
    ]
    
    db.add_documents(test_items)
    print(f"Test data added. Total docs: {db.get_count()}")
    
    # Test query engine
    engine = QueryEngine()
    
    questions = [
        "Who won the India vs Australia series?",
        "How many wickets did Bumrah take?",
        "When is the IPL auction?"
    ]
    
    print("\n" + "="*50)
    print("Testing Query Engine")
    print("="*50)
    
    for q in questions:
        print(f"\nQ: {q}")
        result = engine.answer_with_sources(q)
        print(f"A: {result['answer']}")
        print(f"Sources: {[s['headline'][:30] + '...' for s in result['sources']]}")