from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager

from backend.config import APP_NAME, APP_VERSION
from backend.services.data_service import data_service_instance
from backend.models.ml_model import ml_model_instance
from backend.routers import graph_metrics, predictions, explorer

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Load data and model
    print(f"Starting {APP_NAME}...")
    data_service_instance.load_data()
    ml_model_instance.load()
    yield
    # Shutdown
    print(f"Shutting down {APP_NAME}...")

app = FastAPI(title=APP_NAME, version=APP_VERSION, lifespan=lifespan)

# CORS middleware to allow Streamlit frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(graph_metrics.router, prefix="/api")
app.include_router(predictions.router, prefix="/api")
app.include_router(explorer.router, prefix="/api")

@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "data_loaded": data_service_instance.is_loaded,
        "model_loaded": ml_model_instance.is_loaded
    }

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
