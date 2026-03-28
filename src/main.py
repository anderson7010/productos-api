"""Main FastAPI application for the Product API."""

from fastapi import FastAPI
from src.database import create_tables
from src.routers.product_router import router as product_router

# Create FastAPI application instance
app = FastAPI(
    title="Product API",
    description="A REST API for managing products with CRUD operations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Include product router
app.include_router(product_router)

# Create database tables on startup
@app.on_event("startup")
def startup_event() -> None:
    """Initialize database tables on application startup."""
    create_tables()

# Health check endpoint
@app.get("/", tags=["health"])
def read_root() -> dict[str, str]:
    """Health check endpoint.
    
    Returns:
        Dictionary with status message
    """
    return {"message": "Product API is running"}

# Health check endpoint
@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    """Health check endpoint.
    
    Returns:
        Dictionary with health status
    """
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)