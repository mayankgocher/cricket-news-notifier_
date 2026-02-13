"""
Start Services - Runs FastAPI backend and Telegram bot together
This is needed because Render free tier only allows 1 web service
"""

import os
import sys
import asyncio
import threading
import uvicorn
from multiprocessing import Process

def run_fastapi():
    """Run FastAPI backend"""
    port = int(os.getenv("PORT", 8000))
    print(f"🚀 Starting FastAPI on port {port}...")
    
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )

def run_telegram_bot():
    """Run Telegram bot"""
    print("🤖 Starting Telegram bot...")
    
    # Import here to avoid circular imports
    from telegram_bot import main
    
    try:
        main()
    except Exception as e:
        print(f"⚠️ Telegram bot error: {e}")

def run_scheduler():
    """Run APScheduler for daily jobs"""
    print("🕐 Starting scheduler...")
    
    from scheduler.jobs import start_scheduler
    
    try:
        scheduler = start_scheduler()
        # Keep scheduler running
        import time
        while True:
            time.sleep(60)
    except Exception as e:
        print(f"⚠️ Scheduler error: {e}")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🏏 CRICKET NEWS NOTIFIER - Starting All Services")
    print("="*60)
    
    # Start Telegram bot in a separate thread
    telegram_thread = threading.Thread(target=run_telegram_bot, daemon=True)
    telegram_thread.start()
    print("✅ Telegram bot thread started")
    
    # Start scheduler in a separate thread
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    print("✅ Scheduler thread started")
    
    # Run FastAPI in main thread (blocks here)
    print("✅ Starting FastAPI...")
    run_fastapi()