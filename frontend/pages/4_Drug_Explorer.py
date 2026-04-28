import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# --- end sys.path fix ---

import streamlit as st
import requests
import os
from frontend.components.tables import show_generic_table
from frontend.components.network_graph import create_2d_network, create_3d_network

def load_css():
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "styles", "custom.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()
API_URL = st.secrets.get("API_URL", "http://localhost:8000/api")

st.title("💊 Drug & Disease Explorer")
st.markdown("Select any node from the Biomedical Knowledge Graph to inspect its profile, graph metrics, connections, and real-time interactive visualizations.")

st.markdown("---")

@st.cache_data(ttl=300, show_spinner="Loading node registry...")
def fetch_node_list():
    try:
        r = requests.get(f"{API_URL}/explorer/nodes?limit=25000", timeout=30)
        if r.status_code == 200:
            return {f"{n['name']}  —  {n['id']}": n['id'] for n in r.json()}
    except Exception:
        pass
    return {}

nodes = fetch_node_list()

if not nodes:
    st.error("Could not load node registry from the backend.")
    st.stop()

selected_label = st.selectbox(
    "Select Node", [""] + list(nodes.keys()),
    help="Type to search by name or ID"
)

if not selected_label:
    st.stop()

node_id = nodes[selected_label]

# Fetch node details and ego-graph in parallel (cached)
@st.cache_data(ttl=120)
def fetch_node_detail(nid):
    try:
        r = requests.get(f"{API_URL}/explorer/nodes/{nid}", timeout=10)
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None

@st.cache_data(ttl=120)
def fetch_ego_graph(nid, max_n=30):
    try:
        r = requests.get(f"{API_URL}/explorer/ego-graph/{nid}?max_neighbors={max_n}", timeout=15)
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None

with st.spinner("Fetching node data..."):
    details = fetch_node_detail(node_id)
    ego    = fetch_ego_graph(node_id)

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
    tab2d, tab3d = st.tabs(["📐 2D Network", "🌐 3D Network"])
    with tab2d:
        fig2d = create_2d_network(
            ego['nodes'], ego['edges'],
            title=f"2D Ego-Graph — {node['name']}"
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
