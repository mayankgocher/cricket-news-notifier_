"""
Chat Router - Handles RAG chat endpoints
"""

from fastapi import APIRouter, HTTPException

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.schemas import ChatRequest, ChatResponse
from src.rag.query_engine import QueryEngine

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)

# Initialize query engine
query_engine = None


def get_query_engine():
    """Get or create query engine instance"""
    global query_engine
    if query_engine is None:
        query_engine = QueryEngine()
    return query_engine


@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Ask a question about cricket news (RAG)
    """
    if not request.question or len(request.question.strip()) < 3:
        raise HTTPException(status_code=400, detail="Question too short")
    
    try:
        engine = get_query_engine()
        answer = engine.answer(request.question)
        
        return ChatResponse(answer=answer)
    
    except Exception as e:
        print(f"⚠️ Chat error: {e}")
        raise HTTPException(status_code=500, detail="Error processing question")


@router.post("/with-sources")
def chat_with_sources(request: ChatRequest):
    """
    Ask a question and get answer with sources
    """
    if not request.question or len(request.question.strip()) < 3:
        raise HTTPException(status_code=400, detail="Question too short")
    
    try:
        engine = get_query_engine()
        result = engine.answer_with_sources(request.question)
        
        return result
    
    except Exception as e:
        print(f"⚠️ Chat error: {e}")
        raise HTTPException(status_code=500, detail="Error processing question")


@router.get("/status")
def chat_status():
    """
    Check RAG system status
    """
    try:
        engine = get_query_engine()
        doc_count = engine.vectordb.get_count()
        
        return {
            "status": "online",
            "documents_indexed": doc_count
        }
    
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }