import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# --- end sys.path fix ---

import streamlit as st
import requests
import pandas as pd
import os
from frontend.components.charts import create_distribution_chart
from frontend.components.tables import show_generic_table

@st.cache_data(show_spinner=False)
def get_css():
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "styles", "custom.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            return f.read()
    return ""

st.markdown(f"<style>{get_css()}</style>", unsafe_allow_html=True)
from frontend.components.sidebar import render_sidebar
from frontend.components.page_header import render_page_header
from frontend.components.particles import render_particles
from frontend.utils.api_cache import fetch_distribution, fetch_top_nodes, fetch_communities

render_sidebar()
render_particles()

API_URL = st.secrets.get("API_URL", "http://localhost:8000/api")

render_page_header(
    "Graph Analytics",
    "graph_analytics",
    "Explore the topological structure of the Biomedical Knowledge Graph."
)

st.markdown("---")

# ── Metric Selector ──
metric_labels = {
    'pagerank': 'PageRank',
    'betweenness': 'Betweenness Centrality',
    'eigenvector': 'Eigenvector Centrality',
    'clustering': 'Clustering Coefficient',
    'louvain': 'Louvain Community'
}
selected_metric = st.selectbox("Select Metric", list(metric_labels.keys()), format_func=lambda x: metric_labels[x])

st.markdown("---")

# ── Distribution + Top Nodes ──
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown(f"### {metric_labels[selected_metric]} Distribution")
    dist = fetch_distribution(selected_metric)
    if dist:
        fig = create_distribution_chart(dist, selected_metric)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Distribution data unavailable.")

with col2:
    st.markdown(f"### Top 100 Nodes")
    top = fetch_top_nodes(selected_metric)
    if top:
        show_generic_table(top)
    else:
        st.info("Top nodes data unavailable.")

# ── Community Analysis (Louvain only) ──
if selected_metric == 'louvain':
    st.markdown("---")
    st.markdown("### Louvain Community Sizes")
    try:
        comm_data = fetch_communities()
        if comm_data:
            comm_df = pd.DataFrame(comm_data)
            st.bar_chart(comm_df.set_index('community')['size'], use_container_width=True)
    except Exception as e:
        st.error(f"Error: {e}")
