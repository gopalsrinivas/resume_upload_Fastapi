from fastapi import FastAPI
from app.core.logging import logging
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
import uvicorn
from app.routes.careersRoutes import router as careers_router

# Initialize FastAPI app
app = FastAPI(
    title="FastAPI Resume Upload Application",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
)

# Include router for careers API
app.include_router(careers_router, prefix="/api/v1/careers", tags=["Careers"])


# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Hi, I am FastApi-JWT_Auth. Awesome - Your setup is done & working."
    }


# Startup event
@app.on_event("startup")
async def startup_event():
    logging.info("Application startup application...")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logging.info("Shutting down application...")


# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok"}


# Logging setup and uvicorn run (only one block needed)
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    uvicorn.run(app, host="0.0.0.0", port=8000)
