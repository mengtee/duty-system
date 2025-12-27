
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.database import Database
from api.staff_routes import router as staff_router
from api.schedule_routes import router as schedule_router
from api.statistics_routes import router as statistics_router
from api.export_routes import router as export_router
from api.auto_schedule_routes import router as auto_schedule_router

# Create FastAPI app
app = FastAPI(
    title="Shift duty system",
    description="API for managing staff shifts and schedules",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(staff_router)
app.include_router(schedule_router)
app.include_router(statistics_router)
app.include_router(export_router)
app.include_router(auto_schedule_router)

@app.on_event("startup")
def startup_event():
    """Initialize database on startup."""
    Database.create_tables()
    print("✅ Database tables created")

@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "Shift Management System API",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)
