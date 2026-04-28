import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# --- end sys.path fix ---

import streamlit as st
import requests
import pandas as pd
import os
from frontend.components.charts import create_feature_importance_chart, create_gauge_chart
from frontend.components.tables import show_discoveries_table
from frontend.components.network_graph import create_2d_network

def load_css():
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "styles", "custom.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()
from frontend.components.sidebar import render_sidebar
render_sidebar()

API_URL = st.secrets.get("API_URL", "http://localhost:8000/api")

st.title("🤖 ML Predictions & Discoveries")
st.markdown("Analyze the Random Forest classifier and explore novel drug-disease repurposing candidates.")

st.markdown("---")

# ═══════════════════════════════════════════════
# Section 1 — Feature Importance
# ═══════════════════════════════════════════════
@st.cache_data(ttl=300)
def fetch_model_metrics():
    try:
        r = requests.get(f"{API_URL}/predictions/model-metrics", timeout=10)
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None

model_data = fetch_model_metrics()

if model_data:
    st.markdown("### Feature Importance")
    fig = create_feature_importance_chart(model_data.get('feature_importance', []))
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Model metrics are not available.")

st.markdown("---")

# ═══════════════════════════════════════════════
# Section 2 — Novel Drug Repurposing Discoveries
# ═══════════════════════════════════════════════
st.markdown("### 🔍 Novel Drug Repurposing Discoveries")
st.markdown(
    "Adjust the confidence threshold to explore predicted links between Compounds and Diseases "
    "that **do not currently exist** in the Knowledge Graph."
)

@st.cache_data(ttl=600, show_spinner="Loading discovery candidates from model...")
def fetch_all_discoveries():
    """Fetch ALL discovery candidates from the backend once, then filter locally."""
    try:
        r = requests.get(f"{API_URL}/predictions/discoveries?threshold=0.0&limit=50000", timeout=60)
        if r.status_code == 200:
            data = r.json()
            if data:
                return pd.DataFrame(data)
    except Exception:
        pass
    return pd.DataFrame()

all_disc = fetch_all_discoveries()

col_ctrl, col_table = st.columns([1, 3], gap="large")

with col_ctrl:
    threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.50, 0.05)
    show_all = st.checkbox("Show all results", value=False, help="By default only the Top 100 are shown")

if not all_disc.empty:
    filtered = all_disc[all_disc['predicted_probability'] >= threshold].sort_values('predicted_probability', ascending=False)
    with col_ctrl:
        st.metric("Candidates Found", f"{len(filtered):,}")
    with col_table:
        if len(filtered) > 0:
            display = filtered if show_all else filtered.head(100)
            show_discoveries_table(display.to_dict('records'))
        else:
            st.info("No candidates at this threshold. Lower the slider to discover more.")
else:
    with col_table:
        st.error("Could not load discovery candidates. Make sure the backend API is running and try refreshing the page.")

st.markdown("---")

# ═══════════════════════════════════════════════
# Section 3 — Real-time Pair Prediction
# ═══════════════════════════════════════════════
st.markdown("### 🧪 Real-time Pair Prediction")
st.markdown("Select a Compound and a Disease to get an instant ML confidence score.")

@st.cache_data(ttl=300)
def fetch_node_options(kind):
    try:
        r = requests.get(f"{API_URL}/explorer/nodes?kind={kind}&limit=1000", timeout=10)
        if r.status_code == 200:
            return {f"{n['name']}  —  {n['id']}": n['id'] for n in r.json()}
    except Exception:
        pass
    return {}

compounds = fetch_node_options("Compound")
diseases = fetch_node_options("Disease")

p1, p2, p3 = st.columns([2, 2, 1], gap="medium")
with p1:
    comp_key = st.selectbox("Compound", list(compounds.keys()) if compounds else ["No data"])
with p2:
    dis_key = st.selectbox("Disease", list(diseases.keys()) if diseases else ["No data"])
with p3:
    st.write("")
    st.write("")
    run = st.button("Predict Link", type="primary", use_container_width=True)

if run and compounds and diseases:
    comp_id = compounds[comp_key]
    dis_id  = diseases[dis_key]
    payload = {"compound_id": comp_id, "disease_id": dis_id}
    try:
        r = requests.post(f"{API_URL}/predictions/", json=payload, timeout=10)
        if r.status_code == 200:
            result = r.json()
            r1, r2 = st.columns(2)
            with r1:
                st.plotly_chart(create_gauge_chart(result['probability']), use_container_width=True)
            with r2:
                st.markdown("#### Feature Vector")
                st.json(result['feature_values'])

            # ── Relationship Graph ──────────────────────
            st.markdown("#### Relationship Graph")
            st.caption("The 2D ego-graphs of both nodes overlaid — showing their shared neighborhood.")
            try:
                ego_c = requests.get(f"{API_URL}/explorer/ego-graph/{comp_id}?max_neighbors=20", timeout=10).json()
                ego_d = requests.get(f"{API_URL}/explorer/ego-graph/{dis_id}?max_neighbors=20", timeout=10).json()

                # Merge both ego graphs
                merged_nodes = {n['id']: n for n in ego_c.get('nodes', []) + ego_d.get('nodes', [])}
                merged_edges = ego_c.get('edges', []) + ego_d.get('edges', [])

                fig_rel = create_2d_network(
                    list(merged_nodes.values()), merged_edges,
                    title=f"Relationship: {comp_key.split('—')[0].strip()} ↔ {dis_key.split('—')[0].strip()}"
                )
                st.plotly_chart(fig_rel, use_container_width=True)
            except Exception:
                st.info("Relationship graph unavailable.")
        else:
            st.error(f"Prediction failed: {r.json().get('detail', 'Unknown error')}")
    except Exception as e:
        st.error(f"Request failed: {e}")

