from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any
from backend.models.schemas import NodeInfo, EdgeInfo
from backend.services.data_service import data_service_instance

router = APIRouter(prefix="/explorer", tags=["Knowledge Graph Explorer"])

@router.get("/nodes", response_model=List[NodeInfo])
def search_nodes(search: str = "", kind: str = None, limit: int = 50):
    return data_service_instance.search_nodes(search, kind, limit)

@router.get("/ego-graph/{node_id}")
def get_ego_graph(node_id: str, max_neighbors: int = 30):
    """Return the ego-graph for a node: the node itself + its immediate neighbors + edges."""
    result = data_service_instance.get_ego_graph(node_id, max_neighbors)
    if not result['nodes']:
        raise HTTPException(status_code=404, detail="Node not found")
    return result

@router.get("/k-hop-graph/{node_id}")
def get_k_hop_graph(node_id: str, depth: int = 1, limit: int = 20):
    """Return a graph with neighbors up to depth K."""
    return data_service_instance.get_k_hop_graph(node_id, depth, limit)

@router.get("/relationship-graph/{node_a}/{node_b}")
def get_relationship_graph(node_a: str, node_b: str, shared: int = 20, unique: int = 10):
    """Return a combined graph showing shared and unique neighbors between two nodes."""
    return data_service_instance.get_relationship_graph(node_a, node_b, shared, unique)

@router.get("/nodes/{node_id}")
def get_node_detail(node_id: str):
    node = data_service_instance.get_node(node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    
    metrics = data_service_instance.get_graph_metrics(node_id)
    edges = data_service_instance.get_node_edges(node_id)
    
    return {
        "node": node,
        "metrics": metrics,
        "edges": edges
    }

@router.get("/edges", response_model=List[EdgeInfo])
def get_edges(source: str = None, target: str = None, limit: int = 100):
    if not source and not target:
        raise HTTPException(status_code=400, detail="Must provide source or target node_id")
        
    results = []
    if source:
        edges = data_service_instance.edges[data_service_instance.edges['source'] == source]
        if target:
            edges = edges[edges['target'] == target]
        results = edges.head(limit).to_dict('records')
    elif target:
        edges = data_service_instance.edges[data_service_instance.edges['target'] == target]
        results = edges.head(limit).to_dict('records')
        
    return results

@router.get("/stats")
def get_graph_stats():
    node_kinds = data_service_instance.nodes['kind'].value_counts().to_dict()
    edge_types = data_service_instance.edges['metaedge'].value_counts().to_dict()
    
    return {
        "total_nodes": len(data_service_instance.nodes),
        "total_edges": len(data_service_instance.edges),
        "node_kinds": node_kinds,
        "edge_types": edge_types
    }
