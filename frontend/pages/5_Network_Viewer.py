import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# --- end sys.path fix ---

import streamlit as st
import os

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

render_sidebar()
render_particles()

render_page_header(
    "Network Viewer",
    "network_viewer",
    "Interactive 3D visualization of the Biomedical Knowledge Graph communities and hub nodes."
)

st.markdown("---")

# Subgraph visuals
st.markdown("### Subgraph Visualizations")
assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
col_a, col_b = st.columns(2, gap="large")
img1 = os.path.join(assets_dir, "subgraph_hubs.png")
img2 = os.path.join(assets_dir, "community_clusters.png")
with col_a:
    if os.path.exists(img1):
        st.image(img1, caption="Hub Sub-network", use_container_width=True)
with col_b:
    if os.path.exists(img2):
        st.image(img2, caption="Community Clusters", use_container_width=True)

st.markdown("---")
st.markdown("### Interactive 3D Network")
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
html_path = os.path.join(base_dir, "interactive_3d_network_isolated.html")
if os.path.exists(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        st.components.v1.html(f.read(), height=700, scrolling=True)
else:
    st.info("3D network file not found.")

st.markdown("---")
st.markdown("### Louvain Hub Analysis")
c1, c2 = st.columns(2, gap="large")
p1 = os.path.join(base_dir, "louvain_hubs_rank_1_to_3.png")
p2 = os.path.join(base_dir, "louvain_hubs_rank_4_to_6.png")
with c1:
    if os.path.exists(p1):
        st.image(p1, caption="Top Hubs Rank 1-3", use_container_width=True)
with c2:
    if os.path.exists(p2):
        st.image(p2, caption="Top Hubs Rank 4-6", use_container_width=True)
