from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any, Union

class NodeInfo(BaseModel):
    id: str
    name: str
    kind: str
    out_degree: int
    in_degree: int

class EdgeInfo(BaseModel):
    source: str
    metaedge: str
    target: str

class GraphMetrics(BaseModel):
    id: str
    pagerank: float
    betweenness: float
    eigenvector: float
    louvain: int
    lpa: int
    clustering: float

class PredictionRequest(BaseModel):
    compound_id: str
    disease_id: str

class PredictionResponse(BaseModel):
    compound_id: str
    disease_id: str
    probability: float
    prediction: int
    feature_values: Dict[str, float]

class ModelMetrics(BaseModel):
    metrics: Dict[str, List[Any]]
    feature_importance: List[Dict[str, Union[str, float]]]
    features: List[str]

class DiscoveryCandidate(BaseModel):
    source: str
    source_name: str
    target: str
    target_name: str
    predicted_probability: float
    # Include some graph features for context
    compound_pagerank: float
    disease_pagerank: float
    same_louvain_community: int
