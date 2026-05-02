import streamlit as st
import requests
import pandas as pd

API_URL = st.secrets.get("API_URL", "http://localhost:8000/api")

# ── Explorer & Detail Caching ──
@st.cache_data(ttl=300, show_spinner=False)
def fetch_node_detail(node_id):
    try:
        r = requests.get(f"{API_URL}/explorer/nodes/{node_id}", timeout=10)
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None

@st.cache_data(ttl=300, show_spinner=False)
def fetch_ego_graph(node_id, max_n=30):
    try:
        r = requests.get(f"{API_URL}/explorer/ego-graph/{node_id}?max_neighbors={max_n}", timeout=15)
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None

@st.cache_data(ttl=300, show_spinner=False)
def fetch_relationship_graph(node_a, node_b):
    try:
        r = requests.get(f"{API_URL}/explorer/relationship-graph/{node_a}/{node_b}", timeout=20)
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None

@st.cache_data(ttl=300, show_spinner=False)
def fetch_k_hop_graph(node_id, depth=1, limit=30):
    try:
        r = requests.get(f"{API_URL}/explorer/k-hop-graph/{node_id}?depth={depth}&limit={limit}", timeout=25)
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None

# ── Prediction Caching ──
@st.cache_data(ttl=300, show_spinner=False)
def fetch_prediction(comp_id, dis_id):
    try:
        payload = {"compound_id": comp_id, "disease_id": dis_id}
        r = requests.post(f"{API_URL}/predictions/", json=payload, timeout=10)
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None

# ── Graph Analytics Caching ──
@st.cache_data(ttl=300, show_spinner=False)
def fetch_graph_stats():
    try:
        r = requests.get(f"{API_URL}/explorer/stats", timeout=10)
        if r.status_code == 200:
            return r.json()
    except Exception:
        return None
@st.cache_data(ttl=300, show_spinner=False)
def fetch_distribution(metric, bins=50):
    try:
        r = requests.get(f"{API_URL}/graph-metrics/distribution/{metric}?bins={bins}", timeout=10)
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None

@st.cache_data(ttl=300, show_spinner=False)
def fetch_top_nodes(metric, limit=100):
    try:
        r = requests.get(f"{API_URL}/graph-metrics/top/{metric}?limit={limit}", timeout=10)
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None

@st.cache_data(ttl=300, show_spinner=False)
def fetch_communities():
    try:
        r = requests.get(f"{API_URL}/graph-metrics/communities", timeout=10)
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None

# ── ML Predictions Caching ──
@st.cache_data(ttl=300, show_spinner=False)
def fetch_model_metrics():
    try:
        r = requests.get(f"{API_URL}/predictions/model-metrics", timeout=10)
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None

@st.cache_data(ttl=600, show_spinner=False)
def fetch_all_discoveries():
    try:
        r = requests.get(f"{API_URL}/predictions/discoveries?threshold=0.0&limit=50000", timeout=60)
        if r.status_code == 200:
            data = r.json()
            if data:
                return pd.DataFrame(data)
    except Exception:
        pass
    return pd.DataFrame()

@st.cache_data(ttl=300, show_spinner=False)
def fetch_node_options(kind):
    try:
        r = requests.get(f"{API_URL}/explorer/nodes?kind={kind}&limit=1000", timeout=10)
        if r.status_code == 200:
            return {f"{n['name']}  —  {n['id']}": n['id'] for n in r.json()}
    except Exception:
        pass
    return {}

@st.cache_data(ttl=300, show_spinner=False)
def fetch_node_list():
    try:
        r = requests.get(f"{API_URL}/explorer/nodes?limit=25000", timeout=30)
        if r.status_code == 200:
            return {f"{n['name']}  —  {n['id']}": n['id'] for n in r.json()}
    except Exception:
        pass
    return {}

def preload_all_data():
    """Call this function on the main page to cache everything in the background."""
    fetch_graph_stats()
    # Pre-fetch graph metrics
    for metric in ['pagerank', 'betweenness', 'eigenvector', 'clustering', 'louvain']:
        fetch_distribution(metric)
        fetch_top_nodes(metric)
    fetch_communities()
    
    # Pre-fetch ML prediction data
    fetch_model_metrics()
    fetch_all_discoveries()
    fetch_node_options("Compound")
    fetch_node_options("Disease")
    nodes = fetch_node_list()

    # Pre-compute defaults for Drug Explorer and ML Predictions
    if nodes:
        default_node_id = list(nodes.values())[0]
        fetch_node_detail(default_node_id)
        fetch_ego_graph(default_node_id)

    compounds = fetch_node_options("Compound")
    diseases = fetch_node_options("Disease")
    if compounds and diseases:
        c_id = list(compounds.values())[0]
        d_id = list(diseases.values())[0]
        fetch_prediction(c_id, d_id)
        # Pre-cache the relationship graph showing shared neighbors
        fetch_relationship_graph(c_id, d_id)
