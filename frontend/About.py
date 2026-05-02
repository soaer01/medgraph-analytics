import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# --- end sys.path fix ---

import streamlit as st
import requests
import os
from PIL import Image

# ── Page Config ──
_favicon_path = os.path.join(os.path.dirname(__file__), "assets", "favicon.png")
_favicon = Image.open(_favicon_path) if os.path.exists(_favicon_path) else "🧬"

st.set_page_config(
    page_title="About — MedGraph-Analytics",
    page_icon=_favicon,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Load CSS ──
@st.cache_data(show_spinner=False)
def get_css():
    css_path = os.path.join(os.path.dirname(__file__), "styles", "custom.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            return f.read()
    return ""

st.markdown(f"<style>{get_css()}</style>", unsafe_allow_html=True)
API_URL = st.secrets.get("API_URL", "http://localhost:8000/api")

from frontend.components.sidebar import render_sidebar
from frontend.components.page_header import render_page_header
from frontend.components.particles import render_particles
from frontend.utils.api_cache import preload_all_data
from streamlit.runtime.scriptrunner import add_script_run_ctx
import threading

render_sidebar()
render_particles()

# Preload data in background without blocking
if 'preloaded' not in st.session_state:
    st.session_state.preloaded = True
    def run_preload():
        try:
            preload_all_data()
        except Exception:
            pass
    t = threading.Thread(target=run_preload, daemon=True)
    add_script_run_ctx(t)
    t.start()

# ── Hero Section ──
render_page_header(
    "MedGraph-Analytics",
    "about",
    "A full-stack biomedical analytics platform integrating Neo4j Graph Data Science "
    "with a fine-tuned Random Forest classifier to predict novel drug-disease repurposing candidates."
)

st.markdown("---")

# ── KPI Row ──
c1, c2, c3, c4 = st.columns(4)
c1.metric("Nodes", "22,635")
c2.metric("Edges", "562,107")
c3.metric("ML Pairs", "1,511")
c4.metric("Best AUC", "0.937")

st.markdown("---")

# ── Visual showcase — generated subgraph images ──
st.markdown("### Knowledge Graph Visualizations")
assets_dir = os.path.join(os.path.dirname(__file__), "assets")

col_a, col_b = st.columns(2)
img_hubs = os.path.join(assets_dir, "subgraph_hubs.png")
img_comm = os.path.join(assets_dir, "community_clusters.png")

with col_a:
    if os.path.exists(img_hubs):
        st.image(img_hubs, caption="Biomedical Knowledge Graph — Hub Sub-network", use_container_width=True)
with col_b:
    if os.path.exists(img_comm):
        st.image(img_comm, caption="Louvain Community Clusters", use_container_width=True)

st.markdown("---")

# ── Features ──
st.markdown("### Platform Capabilities")
f1, f2, f3 = st.columns(3)
with f1:
    st.markdown("""
    <div class="neon-card">
        <h5>Graph Analytics</h5>
        <p>Explore PageRank, Betweenness Centrality, Eigenvector Centrality, and Louvain communities across the full knowledge graph.</p>
    </div>
    """, unsafe_allow_html=True)
with f2:
    st.markdown("""
    <div class="neon-card">
        <h5>ML Discovery</h5>
        <p>Predict novel drug-disease links with an adjustable confidence threshold. View Top 100 candidates or the complete list.</p>
    </div>
    """, unsafe_allow_html=True)
with f3:
    st.markdown("""
    <div class="neon-card">
        <h5>Node Explorer</h5>
        <p>Select any compound or disease from 22,000+ nodes and inspect its profile, graph metrics, and all known connections.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.caption("Powered by FastAPI · Streamlit · Plotly · Scikit-Learn")
