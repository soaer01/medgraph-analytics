import pandas as pd
import numpy as np
from backend.config import ML_DATASET_PATH, GRAPH_METRICS_PATH, NODES_PATH, EDGES_PATH
from backend.models.schemas import NodeInfo, EdgeInfo, GraphMetrics

class DataService:
    def __init__(self):
        self.ml_dataset = None
        self.graph_metrics = None
        self.nodes = None
        self.edges = None
        self.is_loaded = False
        
    def load_data(self):
        print("Loading CSV datasets into memory...")
        self.ml_dataset = pd.read_csv(ML_DATASET_PATH)
        self.graph_metrics = pd.read_csv(GRAPH_METRICS_PATH)
        self.nodes = pd.read_csv(NODES_PATH)
        self.edges = pd.read_csv(EDGES_PATH)
        
        # Optimize search operations by setting indices
        self.graph_metrics.set_index('id', inplace=True)
        self.nodes.set_index('id', inplace=True)
        
        self.is_loaded = True
        print("Data loaded successfully.")

    def get_node(self, node_id: str) -> dict:
        if node_id in self.nodes.index:
            node = self.nodes.loc[node_id].to_dict()
            node['id'] = node_id
            return node
        return None

    def search_nodes(self, query: str, kind: str = None, limit: int = 50) -> list:
        df = self.nodes
        if kind:
            df = df[df['kind'] == kind]
        
        # Case insensitive search in name or id
        query = query.lower()
        mask = df['name'].str.lower().str.contains(query, na=False) | df.index.str.lower().str.contains(query, na=False)
        results = df[mask].head(limit)
        
        return [{"id": idx, **row} for idx, row in results.iterrows()]

    def get_graph_metrics(self, node_id: str) -> dict:
        if node_id in self.graph_metrics.index:
            metrics = self.graph_metrics.loc[node_id].to_dict()
            metrics['id'] = node_id
            return metrics
        return None

    def get_node_edges(self, node_id: str, as_source: bool = True, as_target: bool = True, limit: int = 100) -> list:
        results = []
        if as_source:
            source_edges = self.edges[self.edges['source'] == node_id].head(limit)
            results.extend(source_edges.to_dict('records'))
        if as_target:
            target_edges = self.edges[self.edges['target'] == node_id].head(limit)
            results.extend(target_edges.to_dict('records'))
        return results

    def get_ego_graph(self, node_id: str, max_neighbors: int = 30) -> dict:
        """Return the ego-graph (node + neighbors + connecting edges) for 2D/3D rendering."""
        center_node = self.get_node(node_id)
        if not center_node:
            return {'nodes': [], 'edges': []}

        # Get all edges touching this node
        src_edges = self.edges[self.edges['source'] == node_id].head(max_neighbors)
        tgt_edges = self.edges[self.edges['target'] == node_id].head(max_neighbors)
        all_edges = pd.concat([src_edges, tgt_edges]).drop_duplicates()

        # Collect neighbor IDs
        neighbor_ids = set(all_edges['source'].tolist() + all_edges['target'].tolist())
        neighbor_ids.discard(node_id)

        # Build node list: center first, then neighbors
        nodes = [center_node]
        for nid in list(neighbor_ids)[:max_neighbors]:
            n = self.get_node(nid)
            if n:
                nodes.append(n)

        edges = all_edges[['source', 'target', 'metaedge']].to_dict('records')
        return {'nodes': nodes, 'edges': edges}

    def get_all_graph_metrics_paginated(self, skip: int = 0, limit: int = 100) -> list:
        subset = self.graph_metrics.iloc[skip:skip+limit]
        return [{"id": idx, **row} for idx, row in subset.iterrows()]
        
    def get_metric_distribution(self, metric: str, bins: int = 50) -> dict:
        if metric not in self.graph_metrics.columns:
            return None
        
        counts, bin_edges = np.histogram(self.graph_metrics[metric].dropna(), bins=bins)
        return {
            "counts": counts.tolist(),
            "bin_edges": bin_edges.tolist()
        }

    def get_top_nodes_by_metric(self, metric: str, limit: int = 100) -> list:
        if metric not in self.graph_metrics.columns:
            return None
            
        top_df = self.graph_metrics.sort_values(by=metric, ascending=False).head(limit)
        
        # Join with node info to get names
        results = []
        for idx, row in top_df.iterrows():
            node_info = self.get_node(idx)
            name = node_info['name'] if node_info else 'Unknown'
            kind = node_info['kind'] if node_info else 'Unknown'
            results.append({
                "id": idx,
                "name": name,
                "kind": kind,
                "metric_value": row[metric]
            })
            
        return results

    def get_louvain_communities(self, limit: int = 50) -> list:
        # Count nodes per community
        community_counts = self.graph_metrics['louvain'].value_counts().head(limit)
        return [{"community": int(k), "size": int(v)} for k, v in community_counts.items()]

data_service_instance = DataService()
