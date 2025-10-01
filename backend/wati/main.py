from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import select, func
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Temporarily commenting out all imports to isolate 502 error
# from .database import database
# from .routes import user, broadcast, contacts, auth, woocommerce, integration, wallet, analytics, ai
# from .services import dramatiq_router
# from . import oauth2
# from .models import ChatBox

# Create FastAPI app instance
app = FastAPI(title="Wotnot AI Template System", version="1.0.0")
scheduler = AsyncIOScheduler()
scheduler_started = False

# Models creation - temporarily disabled for 502 debugging
async def create_db_and_tables():
    print("Database creation skipped for debugging")
    pass

# Adding the routes - temporarily commented out to isolate 502 error
# app.include_router(broadcast.router)
# app.include_router(contacts.router)
# app.include_router(user.router)
# app.include_router(auth.router)
# app.include_router(wallet.router)
# app.include_router(oauth2.router)
# app.include_router(dramatiq_router.router)
# app.include_router(woocommerce.router)
# app.include_router(integration.router)
# app.include_router(analytics.router)
# app.include_router(ai.router)

# Railway health check endpoints
@app.get("/")
def read_root():
    return {"message": "Wotnot AI Template System API", "status": "running", "docs": "/docs"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "wotnot-backend", "timestamp": datetime.now().isoformat()}

# Defining origins for CORS


# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chat cleanup scheduler setup


# Temporarily commented out chat cleanup function to isolate 502 error
async def close_expired_chats() -> None:
    """
    Close chats that have been inactive for more than 5 minutes.
    """
    try:
        print("Chat cleanup function called")
        # Temporarily disabled to isolate startup issues
        pass
    except Exception as e:
        # Log the error
        print(f"Error in close_expired_chats: {e}")


@app.on_event("startup")
async def startup_event() -> None:
    """
    Event triggered when the application starts.
    Minimal startup - bypassing database for 502 debugging.
    """
    try:
        print("Minimal startup - database and scheduler disabled for debugging")
        print("FastAPI app should now respond to basic endpoints")
    except Exception as e:
        print(f"Startup error: {e}")


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """
    Event triggered when the application shuts down.
    Properly stops the scheduler to clean up resources.
    """
    global scheduler_started
    if scheduler_started:
        scheduler.shutdown(wait=False)  # Ensures shutdown is non-blocking
        scheduler_started = False
        print("Scheduler shut down.")
