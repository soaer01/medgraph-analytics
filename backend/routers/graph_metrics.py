from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any
from backend.models.schemas import GraphMetrics
from backend.services.data_service import data_service_instance

router = APIRouter(prefix="/graph-metrics", tags=["Graph Metrics"])

@router.get("/", response_model=List[GraphMetrics])
def get_graph_metrics(skip: int = 0, limit: int = Query(default=100, le=1000)):
    return data_service_instance.get_all_graph_metrics_paginated(skip, limit)

@router.get("/distribution/{metric}", response_model=Dict[str, List[float]])
def get_metric_distribution(metric: str, bins: int = 50):
    result = data_service_instance.get_metric_distribution(metric, bins)
    if not result:
        raise HTTPException(status_code=404, detail="Metric not found")
    return result

@router.get("/top/{metric}", response_model=List[Dict[str, Any]])
def get_top_nodes(metric: str, limit: int = 100):
    result = data_service_instance.get_top_nodes_by_metric(metric, limit)
    if not result:
        raise HTTPException(status_code=404, detail="Metric not found")
    return result

@router.get("/communities", response_model=List[Dict[str, int]])
def get_communities(limit: int = 50):
    return data_service_instance.get_louvain_communities(limit)

@router.get("/{node_id}", response_model=GraphMetrics)
def get_node_metrics(node_id: str):
    metrics = data_service_instance.get_graph_metrics(node_id)
    if not metrics:
        raise HTTPException(status_code=404, detail="Node metrics not found")
    return metrics
