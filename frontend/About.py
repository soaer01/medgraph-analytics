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
def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "styles", "custom.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()
API_URL = st.secrets.get("API_URL", "http://localhost:8000/api")

from frontend.components.sidebar import render_sidebar
from frontend.components.page_header import render_page_header
from frontend.components.particles import render_particles

render_sidebar()
render_particles()

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
    st.markdown("##### Graph Analytics")
    st.markdown("Explore PageRank, Betweenness Centrality, Eigenvector Centrality, and Louvain communities across the full knowledge graph.")
with f2:
    st.markdown("##### ML Discovery")
    st.markdown("Predict novel drug-disease links with an adjustable confidence threshold. View Top 100 candidates or the complete list.")
with f3:
    st.markdown("##### Node Explorer")
    st.markdown("Select any compound or disease from 22,000+ nodes and inspect its profile, graph metrics, and all known connections.")

st.markdown("---")
st.caption("Powered by FastAPI · Streamlit · Plotly · Scikit-Learn")
