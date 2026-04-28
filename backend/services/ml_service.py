import pandas as pd
import numpy as np
import json
from backend.models.ml_model import ml_model_instance
from backend.services.data_service import data_service_instance
from backend.config import METRICS_PATH, GRAPH_METRICS_PATH
import os

class MLService:
    
    def __init__(self):
        self._discoveries_cache = None
    
    def predict_pair(self, compound_id: str, disease_id: str) -> dict:
        compound_node = data_service_instance.get_node(compound_id)
        disease_node = data_service_instance.get_node(disease_id)
        
        if not compound_node or not disease_node:
            raise ValueError("Compound or Disease not found")
            
        compound_metrics = data_service_instance.get_graph_metrics(compound_id)
        disease_metrics = data_service_instance.get_graph_metrics(disease_id)
        
        if not compound_metrics or not disease_metrics:
            raise ValueError("Graph metrics not available for Compound or Disease")
            
        same_louvain = 1 if compound_metrics.get('louvain') == disease_metrics.get('louvain') else 0
        
        feature_dict = {
            'compound_out_degree': compound_node.get('out_degree', 0),
            'compound_in_degree': compound_node.get('in_degree', 0),
            'disease_out_degree': disease_node.get('out_degree', 0),
            'disease_in_degree': disease_node.get('in_degree', 0),
            'compound_pagerank': compound_metrics.get('pagerank', 0),
            'disease_pagerank': disease_metrics.get('pagerank', 0),
            'compound_betweenness': compound_metrics.get('betweenness', 0),
            'disease_betweenness': disease_metrics.get('betweenness', 0),
            'compound_eigenvector': compound_metrics.get('eigenvector', 0),
            'disease_eigenvector': disease_metrics.get('eigenvector', 0),
            'compound_clustering': compound_metrics.get('clustering', 0),
            'disease_clustering': disease_metrics.get('clustering', 0),
            'same_louvain_community': same_louvain
        }
        
        feature_df = pd.DataFrame([feature_dict])
        prediction, probability = ml_model_instance.predict(feature_df)
        
        return {
            "compound_id": compound_id,
            "disease_id": disease_id,
            "prediction": int(prediction),
            "probability": float(probability),
            "feature_values": feature_dict
        }
        
    def get_model_metrics(self):
        if os.path.exists(METRICS_PATH):
            with open(METRICS_PATH, 'r') as f:
                return json.load(f)
        return None

    def _build_discoveries(self):
        """Build and cache the full discoveries table by merging graph metrics into the baseline dataset."""
        df = data_service_instance.ml_dataset.copy()
        graph_metrics = pd.read_csv(GRAPH_METRICS_PATH)
        
        # Merge compound metrics
        df = df.merge(graph_metrics, left_on='source', right_on='id', how='left').rename(columns={
            'pagerank': 'compound_pagerank', 'betweenness': 'compound_betweenness',
            'eigenvector': 'compound_eigenvector', 'louvain': 'compound_louvain',
            'lpa': 'compound_lpa', 'clustering': 'compound_clustering'
        }).drop(columns=['id'], errors='ignore')
        
        # Merge disease metrics
        df = df.merge(graph_metrics, left_on='target', right_on='id', how='left').rename(columns={
            'pagerank': 'disease_pagerank', 'betweenness': 'disease_betweenness',
            'eigenvector': 'disease_eigenvector', 'louvain': 'disease_louvain',
            'lpa': 'disease_lpa', 'clustering': 'disease_clustering'
        }).drop(columns=['id'], errors='ignore')
        
        df['same_louvain_community'] = (df['compound_louvain'] == df['disease_louvain']).astype(int)
        df.fillna(0, inplace=True)
        
        # Only predict on negative (label == 0) pairs
        negatives = df[df['label'] == 0].copy()
        
        if negatives.empty:
            self._discoveries_cache = pd.DataFrame()
            return
        
        graph_features = [
            'compound_out_degree', 'compound_in_degree', 'disease_out_degree', 'disease_in_degree',
            'compound_pagerank', 'disease_pagerank', 'compound_betweenness', 'disease_betweenness',
            'compound_eigenvector', 'disease_eigenvector', 'compound_clustering', 'disease_clustering',
            'same_louvain_community'
        ]
        
        X_pred = negatives[graph_features]
        probabilities = ml_model_instance.model.predict_proba(X_pred)[:, 1]
        negatives['predicted_probability'] = probabilities
        
        self._discoveries_cache = negatives.sort_values(by='predicted_probability', ascending=False)
        print(f"Discoveries cache built: {len(self._discoveries_cache)} candidates")

    def get_discoveries(self, threshold: float = 0.5, limit: int = 100):
        if self._discoveries_cache is None:
            self._build_discoveries()
        
        if self._discoveries_cache.empty:
            return []
        
        filtered = self._discoveries_cache[self._discoveries_cache['predicted_probability'] >= threshold].head(limit)
        
        results = []
        for _, row in filtered.iterrows():
            results.append({
                "source": row['source'],
                "target": row['target'],
                "predicted_probability": float(row['predicted_probability']),
                "compound_pagerank": float(row.get('compound_pagerank', 0)),
                "disease_pagerank": float(row.get('disease_pagerank', 0)),
                "same_louvain_community": int(row.get('same_louvain_community', 0))
            })
            
        return results

ml_service_instance = MLService()
