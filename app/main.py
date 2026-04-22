from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import kinases, structures, substrates

app = FastAPI(
    title="Kinopedia API",
    description="Backend API for kinase database with FastAPI. Includes business logic for pseudokinase enforcement and disputed kinase activity handling.",
    version="1.0.0",
    contact={
        "name": "Sakshi Dhumma",
        "email": "sakshidhumma2000@gmail.com",
    }
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(kinases.router)
app.include_router(structures.router)
app.include_router(substrates.router)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Kinopedia API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "kinases": "/kinases",
            "substrates": "/substrates",
            "structures": "/structures"
        }
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "1.0.0"}