"""Main FastAPI application for AI Receptionist"""
import os
from fastapi import FastAPI, HTTPException, Depends, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from datetime import datetime
from typing import Optional, List
from dotenv import load_dotenv

from .models.database import create_tables, engine, Base
from .models.user import User
from .services.auth_service import auth_service, get_current_active_user, get_admin_user
from .services.business_service import business_service
from .services.appointment_service import appointment_service
from .services.contact_service import contact_service
from .services.faq_service import faq_service
from .services.chat_service import chat_service
from .services.ai_service import ai_service

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="AI Receptionist API",
    description="AI-powered receptionist system for small businesses",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables on startup
@app.on_event("startup")
def on_startup():
    """Initialize database and create default data"""
    create_tables()
    
    # Create default business if none exists
    db = next(auth_service.db)
    business_service_instance = business_service
    business_service_instance.db = db
    
    if not business_service_instance.get_default_business():
        business_service_instance.create_default_business()
    
    # Create default FAQs for the business
    default_business = business_service_instance.get_default_business()
    if default_business:
        faq_service_instance = faq_service
        faq_service_instance.db = db
        faq_service_instance.create_default_faqs(default_business.id)
    
    # Create default admin user if none exists
    admin_user = db.query(User).filter(User.username == "admin").first()
    if not admin_user:
        auth_service_instance = auth_service
        auth_service_instance.db = db
        auth_service_instance.create_user(
            username="admin",
            email="admin@localhost",
            password="admin123",
            full_name="Administrator",
            role="admin"
        )
    
    print("Database initialized with default data")


@app.on_event("shutdown")
def on_shutdown():
    """Clean up on shutdown"""
    from .models.database import close_db
    close_db()


# Include routers
from .routers import (
    auth_router,
    business_router,
    appointment_router,
    contact_router,
    faq_router,
    chat_router,
    ai_router
)

app.include_router(auth_router.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(business_router.router, prefix="/api/businesses", tags=["Business"])
app.include_router(appointment_router.router, prefix="/api/appointments", tags=["Appointments"])
app.include_router(contact_router.router, prefix="/api/contacts", tags=["Contacts"])
app.include_router(faq_router.router, prefix="/api/faqs", tags=["FAQ"])
app.include_router(chat_router.router, prefix="/api/chat", tags=["Chat"])
app.include_router(ai_router.router, prefix="/api/ai", tags=["AI"])


# WebSocket endpoints
@app.websocket("/ws/customer/{business_id}")
async def customer_websocket(websocket: WebSocket, business_id: int):
    """WebSocket endpoint for customer chat"""
    await chat_service.handle_customer_chat(websocket, business_id)


@app.websocket("/ws/agent/{business_id}/{user_id}")
async def agent_websocket(websocket: WebSocket, business_id: int, user_id: int):
    """WebSocket endpoint for agent chat"""
    await chat_service.handle_agent_chat(websocket, business_id, user_id)


# Health check endpoint
@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Receptionist API",
        "version": "1.0.0",
        "docs": "/api/docs",
        "health": "/api/health"
    }


# API info endpoint
@app.get("/api/info")
async def api_info():
    """Get API information"""
    return {
        "name": "AI Receptionist API",
        "version": "1.0.0",
        "description": "AI-powered receptionist system for small businesses",
        "endpoints": {
            "authentication": "/api/auth",
            "businesses": "/api/businesses",
            "appointments": "/api/appointments",
            "contacts": "/api/contacts",
            "faqs": "/api/faqs",
            "chat": "/api/chat",
            "ai": "/api/ai",
            "websocket": {
                "customer": "/ws/customer/{business_id}",
                "agent": "/ws/agent/{business_id}/{user_id}"
            }
        },
        "features": [
            "AI Chatbot for customer interactions",
            "Appointment scheduling and management",
            "Contact and customer management",
            "FAQ and knowledge base",
            "Real-time chat with WebSocket support",
            "Business configuration and settings"
        ]
    }


# Run the application
if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv('SERVER_HOST', '0.0.0.0')
    port = int(os.getenv('SERVER_PORT', 8000))
    
    print(f"Starting AI Receptionist server on {host}:{port}")
    uvicorn.run(app, host=host, port=port, reload=True)
