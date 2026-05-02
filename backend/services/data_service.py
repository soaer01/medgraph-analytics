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

    def get_k_hop_graph(self, node_id: str, depth: int = 1, max_per_hop: int = 20) -> dict:
        """Fetch neighbors up to K hops away."""
        visited_nodes = {node_id}
        all_edges = pd.DataFrame(columns=['source', 'target', 'metaedge'])
        
        current_hop_nodes = {node_id}
        
        for _ in range(depth):
            if not current_hop_nodes:
                break
            
            # Find all edges connected to any node in current hop
            mask = self.edges['source'].isin(current_hop_nodes) | self.edges['target'].isin(current_hop_nodes)
            hop_edges = self.edges[mask].head(len(current_hop_nodes) * max_per_hop)
            
            if hop_edges.empty:
                break
                
            all_edges = pd.concat([all_edges, hop_edges]).drop_duplicates()
            
            # Next hop nodes are the ones we just found that we haven't visited
            found_nodes = set(hop_edges['source'].tolist() + hop_edges['target'].tolist())
            current_hop_nodes = found_nodes - visited_nodes
            visited_nodes.update(found_nodes)
            
            if len(visited_nodes) > 200: # Safety cap
                break

        # Build final node/edge lists
        nodes = []
        for nid in visited_nodes:
            n = self.get_node(nid)
            if n:
                nodes.append(n)
        
        edges = all_edges[['source', 'target', 'metaedge']].to_dict('records')
        return {'nodes': nodes, 'edges': edges}

    def get_relationship_graph(self, node_a: str, node_b: str, max_shared: int = 50, max_unique: int = 15) -> dict:
        """Return a graph showing shared and unique neighbors between two nodes."""
        na = self.get_node(node_a)
        nb = self.get_node(node_b)
        if not na or not nb:
            return {'nodes': [], 'edges': []}

        # Get neighbors of A
        a_src = self.edges[self.edges['source'] == node_a]['target'].tolist()
        a_tgt = self.edges[self.edges['target'] == node_a]['source'].tolist()
        a_neighbors = set(a_src + a_tgt)

        # Get neighbors of B
        b_src = self.edges[self.edges['source'] == node_b]['target'].tolist()
        b_tgt = self.edges[self.edges['target'] == node_b]['source'].tolist()
        b_neighbors = set(b_src + b_tgt)

        shared_ids = a_neighbors.intersection(b_neighbors)
        only_a = a_neighbors - shared_ids
        only_b = b_neighbors - shared_ids

        # Pick nodes to include
        to_include = {node_a, node_b}
        to_include.update(list(shared_ids)[:max_shared])
        to_include.update(list(only_a)[:max_unique])
        to_include.update(list(only_b)[:max_unique])

        # Fetch node details
        nodes = []
        for nid in to_include:
            n = self.get_node(nid)
            if n:
                nodes.append(n)

        # Fetch all edges between these nodes
        mask = self.edges['source'].isin(to_include) & self.edges['target'].isin(to_include)
        rel_edges = self.edges[mask].to_dict('records')

        return {'nodes': nodes, 'edges': rel_edges}

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
