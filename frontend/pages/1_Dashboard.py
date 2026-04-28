import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# --- end sys.path fix ---

import streamlit as st
import requests
import pandas as pd
import os
from frontend.components.charts import create_donut_chart, create_model_comparison_chart

def load_css():
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "styles", "custom.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()
from frontend.components.sidebar import render_sidebar
from frontend.components.page_header import render_page_header
from frontend.components.particles import render_particles

render_sidebar()
render_particles()

API_URL = st.secrets.get("API_URL", "http://localhost:8000/api")

render_page_header(
    "Executive Dashboard",
    "dashboard",
    "High-level overview of the Biomedical Knowledge Graph structure and ML model performance."
)

st.markdown("---")

# ── Graph Stats ──
@st.cache_data(ttl=300)
def fetch_graph_stats():
    try:
        r = requests.get(f"{API_URL}/explorer/stats", timeout=10)
        if r.status_code == 200:
            return r.json()
    except Exception:
        return None

stats = fetch_graph_stats()

if stats:
    # KPI row
    k1, k2, k3 = st.columns(3)
    k1.metric("Total Nodes", f"{stats['total_nodes']:,}")
    k2.metric("Total Edges", f"{stats['total_edges']:,}")
    k3.metric("Node Types", len(stats['node_kinds']))

    st.markdown("---")

    st.markdown("### Graph Composition")
    col1, col2 = st.columns(2)
    with col1:
        fig1 = create_donut_chart(stats['node_kinds'], "Node Types Distribution")
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        top_edges = dict(list(stats['edge_types'].items())[:6])
        fig2 = create_donut_chart(top_edges, "Top Edge Types")
        st.plotly_chart(fig2, use_container_width=True)
else:
    st.warning("Could not connect to the backend. Is the API server running?")

st.markdown("---")

# ── Model Performance ──
@st.cache_data(ttl=300)
def fetch_model_metrics():
    try:
        r = requests.get(f"{API_URL}/predictions/model-metrics", timeout=10)
        if r.status_code == 200:
            return r.json()
    except Exception:
        return None

model_data = fetch_model_metrics()

if model_data:
    st.markdown("### ML Model Performance")
    metrics = model_data.get('metrics', {})
    fig3 = create_model_comparison_chart(metrics)
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.warning("Model metrics are not available.")
