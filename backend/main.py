"""
Main FastAPI Application - Updated for Render Free Tier
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import engine, Base
from backend.routers import subscribers, newsletters, chat, pipeline

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Cricket News Notifier API",
    description="API for Cricket Daily Digest - News aggregation and notification service",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Include routers
app.include_router(subscribers.router)
app.include_router(newsletters.router)
app.include_router(chat.router)
app.include_router(pipeline.router)


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "name": "Cricket News Notifier API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "docs": "/docs",
            "subscribe": "/subscribers/subscribe",
            "newsletters": "/newsletters/",
            "chat": "/chat/",
            "pipeline": "/pipeline/run",
            "frontend": "/frontend"
        }
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/frontend", response_class=HTMLResponse)
def frontend_page():
    """Frontend landing page"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Cricket News Frontend</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            .card {
                background: white;
                padding: 40px;
                border-radius: 15px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            }
            h1 { color: #1565c0; margin-bottom: 10px; }
            h2 { color: #333; margin-top: 30px; }
            .subtitle { color: #666; font-size: 18px; margin-bottom: 30px; }
            code {
                background: #f0f0f0;
                padding: 3px 8px;
                border-radius: 4px;
                font-family: monospace;
            }
            .button {
                display: inline-block;
                padding: 12px 24px;
                background: #1565c0;
                color: white;
                text-decoration: none;
                border-radius: 6px;
                margin: 10px 5px;
                transition: background 0.3s;
            }
            .button:hover {
                background: #0d47a1;
            }
            ul { line-height: 2; }
            a { color: #1565c0; }
            .status {
                display: inline-block;
                padding: 5px 15px;
                background: #4caf50;
                color: white;
                border-radius: 20px;
                font-size: 14px;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🏏 Cricket Daily Digest</h1>
            <p class="subtitle">Your Daily Source for Cricket News</p>
            <span class="status">✅ API Running</span>
            
            <h2>📡 API Endpoints</h2>
            <ul>
                <li><a href="/docs" target="_blank"><strong>/docs</strong></a> - Interactive API documentation (Swagger UI)</li>
                <li><a href="/health"><strong>/health</strong></a> - Service health check</li>
                <li><a href="/subscribers/count"><strong>/subscribers/count</strong></a> - Get subscriber statistics</li>
                <li><a href="/newsletters/"><strong>/newsletters/</strong></a> - Browse newsletter archive</li>
                <li><strong>/chat/</strong> - RAG-powered cricket Q&A</li>
                <li><strong>/pipeline/run</strong> - Trigger news pipeline</li>
            </ul>
            
            <h2>🤖 Telegram Bot</h2>
            <p>Get cricket news directly on Telegram!</p>
            <ul>
                <li>Search for: <code>@Cricket_daily_digest_bot</code></li>
                <li>Commands: <code>/subscribe</code>, <code>/latest</code>, <code>/status</code></li>
                <li>Ask any cricket question and get AI-powered answers!</li>
            </ul>
            
            <h2>📬 Email Newsletter</h2>
            <p>Subscribe to receive daily cricket digest at 8 AM IST</p>
            <p>Use the API endpoint: <code>POST /subscribers/subscribe</code></p>
            
            <h2>💻 Full Web Interface (Run Locally)</h2>
            <p>Clone the repository to run the Streamlit frontend:</p>
            <code>streamlit run frontend/app.py</code>
            
            <br><br><br>
            <a href="/docs" class="button">📚 API Documentation</a>
            <a href="https://t.me/Cricket_daily_digest_bot" class="button" target="_blank">🤖 Open Telegram Bot</a>
        </div>
    </body>
    </html>
    """


# Run with: uvicorn backend.main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)