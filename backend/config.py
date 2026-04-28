import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'backend' / 'data'

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Data file paths
ML_DATASET_PATH = BASE_DIR / 'baseline_ml_dataset.csv'
GRAPH_METRICS_PATH = BASE_DIR / 'graph_metrics.csv'
NODES_PATH = BASE_DIR / 'neo4j_nodes.csv'
EDGES_PATH = BASE_DIR / 'neo4j_edges.csv'

# Model paths
MODEL_PATH = DATA_DIR / 'trained_model.joblib'
METRICS_PATH = DATA_DIR / 'model_metrics.json'

# Default configurations
DEFAULT_DISCOVERY_THRESHOLD = 0.50
APP_NAME = "MedGraph-Analytics API"
APP_VERSION = "1.0.0"
