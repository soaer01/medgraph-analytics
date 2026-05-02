import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# --- end sys.path fix ---

import streamlit as st
import requests
import os
from PIL import Image

# ── Page Config ──
_favicon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "favicon.png")
_favicon = Image.open(_favicon_path) if os.path.exists(_favicon_path) else "🧬"

st.set_page_config(
    page_title="Drug Explorer — MedGraph",
    page_icon=_favicon,
    layout="wide",
    initial_sidebar_state="expanded",
)
from frontend.components.tables import show_generic_table
from frontend.components.network_graph import create_2d_network, create_3d_network

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
from frontend.utils.api_cache import fetch_node_list, fetch_node_detail, fetch_k_hop_graph

render_sidebar()
render_particles()

API_URL = st.secrets.get("API_URL", "http://localhost:8000/api")

render_page_header(
    "Drug & Disease Explorer",
    "drug_explorer",
    "Select any node from the Biomedical Knowledge Graph to inspect its profile, graph metrics, connections, and real-time interactive visualizations."
)

st.markdown("---")

nodes = fetch_node_list()

if not nodes:
    st.error("Could not load node registry from the backend.")
    st.stop()

selected_label = st.selectbox(
    "Select Node", list(nodes.keys()),
    help="Type to search by name or ID"
)

if not selected_label:
    st.stop()

node_id = nodes[selected_label]

# Fetch node details and ego-graph in parallel (cached)
with st.spinner("Fetching node data..."):
    details = fetch_node_detail(node_id)
    ego    = fetch_k_hop_graph(node_id, depth=1)

if not details:
    st.error("Failed to load node details from the backend.")
    st.stop()

node    = details['node']
metrics = details['metrics']
edges   = details['edges']

st.markdown("---")

# ── Row 1: Profile + Metrics ──────────────────────────────────
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("### Node Profile")
    st.markdown(f"**ID** &nbsp; `{node['id']}`")
    st.markdown(f"**Name** &nbsp; {node['name']}")
    st.markdown(f"**Type** &nbsp; {node['kind']}")
    st.markdown(f"**Out Degree** &nbsp; {node['out_degree']}")
    st.markdown(f"**In Degree** &nbsp; {node['in_degree']}")

with col2:
    st.markdown("### Graph Metrics")
    if metrics:
        m1, m2 = st.columns(2)
        m1.metric("PageRank", f"{metrics.get('pagerank', 0):.6f}")
        m2.metric("Betweenness", f"{metrics.get('betweenness', 0):.2f}")
        m3, m4 = st.columns(2)
        m3.metric("Eigenvector", f"{metrics.get('eigenvector', 0):.2e}")
        m4.metric("Clustering", f"{metrics.get('clustering', 0):.4f}")
        st.metric("Louvain Community", int(metrics.get('louvain', 0)))
    else:
        st.info("No metrics available for this node.")

st.markdown("---")

# ── Row 2: Interactive Network Visualizations ─────────────────
st.markdown("### Interactive Ego-Graph")
st.caption(f"Showing the immediate neighborhood of **{node['name']}** (up to 30 neighbors)")

if ego and ego.get('nodes'):
    tab2d, tab3d = st.tabs(["2D Network", "3D Network"])
    with tab2d:
        fig2d = create_2d_network(
            ego['nodes'], ego['edges'],
            title=f"2D Ego-Graph — {node['name']}",
            focus_ids=[node_id]
        )
        st.plotly_chart(fig2d, use_container_width=True)
        st.caption("🔵 Compound &nbsp;|&nbsp; 🔴 Disease &nbsp;|&nbsp; 🟢 Gene &nbsp;|&nbsp; 🟡 Anatomy &nbsp;|&nbsp; 🟣 Pathway")
    with tab3d:
        fig3d = create_3d_network(
            ego['nodes'], ego['edges'],
            title=f"3D Ego-Graph — {node['name']}"
        )
        st.plotly_chart(fig3d, use_container_width=True)
        st.caption("Rotate: left-drag &nbsp;|&nbsp; Zoom: scroll &nbsp;|&nbsp; Pan: right-drag")
else:
    st.info("Graph data unavailable for this node.")

st.markdown("---")

# ── Row 3: Edge Table ─────────────────────────────────────────
st.markdown("### Known Connections")
if edges:
    st.caption(f"Showing {len(edges)} edge(s)")
    show_generic_table(edges)
else:
    st.info("No edges found for this node.")
