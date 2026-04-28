from fastapi import APIRouter, HTTPException, Query
from typing import List
from backend.models.schemas import PredictionRequest, PredictionResponse, ModelMetrics, DiscoveryCandidate
from backend.services.ml_service import ml_service_instance
from backend.config import DEFAULT_DISCOVERY_THRESHOLD

router = APIRouter(prefix="/predictions", tags=["ML Predictions"])

@router.post("/", response_model=PredictionResponse)
def predict_drug_disease_pair(request: PredictionRequest):
    try:
        result = ml_service_instance.predict_pair(request.compound_id, request.disease_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/model-metrics", response_model=ModelMetrics)
def get_model_metrics():
    metrics = ml_service_instance.get_model_metrics()
    if not metrics:
        raise HTTPException(status_code=404, detail="Model metrics not found")
    return metrics

@router.get("/discoveries", response_model=List[DiscoveryCandidate])
def get_discovery_candidates(threshold: float = Query(default=DEFAULT_DISCOVERY_THRESHOLD, ge=0.0, le=1.0), limit: int = 100):
    try:
        return ml_service_instance.get_discoveries(threshold, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
