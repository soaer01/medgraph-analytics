import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# --- end sys.path fix ---

import streamlit as st
import os

def load_css()
from frontend.components.sidebar import render_sidebar
render_sidebar()
:
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "styles", "custom.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()
from frontend.components.sidebar import render_sidebar
render_sidebar()


st.title("📚 Terminology Reference")
st.markdown(
    "Complete glossary covering every graph metric, ML concept, chart legend, "
    "edge type, node type, and axis label used across this platform."
)

st.markdown("---")

# ─── Dictionary grouped by category ──────────────────────────
TERMS = {

    # ── Graph Metrics ────────────────────────────────────────
    "Graph Metrics": {
        "PageRank": (
            "Measures the transitive importance of a node by propagating influence from its "
            "neighbors. A node with high PageRank is connected to many other high-PageRank nodes. "
            "High-PageRank drugs are considered highly connected 'hub' compounds in the network."
        ),
        "Betweenness Centrality": (
            "The fraction of shortest paths in the entire graph that pass through a node. "
            "Nodes with high betweenness act as bridges between communities; removing them "
            "would fragment the network. Used to identify mediator drugs or diseases."
        ),
        "Eigenvector Centrality": (
            "Measures a node's influence relative to the influence of its neighbors. "
            "Unlike degree centrality, a connection to a highly-connected neighbor contributes "
            "more than a connection to a peripheral node."
        ),
        "Clustering Coefficient": (
            "The proportion of a node's neighbors that are also connected to each other. "
            "High values indicate that the node's neighbors form a tight-knit functional module, "
            "suggesting shared biological roles."
        ),
        "Louvain Community (Community ID)": (
            "An integer label assigned by the Louvain Modularity algorithm identifying which "
            "community (dense sub-network) the node belongs to. Nodes in the same community "
            "share many connections with each other and few with nodes outside."
        ),
        "LPA (Label Propagation Algorithm)": (
            "An alternative community detection method. Each node iteratively adopts the most "
            "common community label among its neighbors until labels stabilize. Faster than "
            "Louvain but less stable on large graphs."
        ),
        "Out Degree": (
            "The number of directed edges leaving a node. For a Compound, it represents "
            "how many biological entities (targets, pathways) it is known to interact with."
        ),
        "In Degree": (
            "The number of directed edges pointing to a node. For a Disease, it represents "
            "how many drugs, genes, or pathways are known to affect it."
        ),
        "same_louvain_community": (
            "A binary feature (0 or 1) used in the ML model. Value = 1 if both the Compound "
            "and Disease belong to the same Louvain community, suggesting they are in the same "
            "biological neighborhood."
        ),
    },

    # ── Node Types (Colors in Network Graphs) ────────────────
    "Node Types — Network Graph Legend": {
        "Compound 🔵": (
            "A small molecule drug or chemical compound (e.g., Metformin, Aspirin). "
            "Displayed in **blue** in the 2D/3D network graphs."
        ),
        "Disease 🔴": (
            "A diagnosed medical condition or disorder (e.g., Type 2 Diabetes, Breast Cancer). "
            "Displayed in **coral/red** in the network graphs."
        ),
        "Gene 🟢": (
            "A gene or gene product (protein) in the human genome (e.g., BRCA1, TP53). "
            "Displayed in **green** in the network graphs."
        ),
        "Anatomy 🟡": (
            "An anatomical location or organ system (e.g., Liver, Lung, Brain). "
            "Displayed in **gold** in the network graphs."
        ),
        "Pathway 🟣": (
            "A biological signaling or metabolic pathway (e.g., MAPK signaling, Apoptosis). "
            "Displayed in **purple** in the network graphs."
        ),
        "Biological Process (teal)": (
            "A GO (Gene Ontology) Biological Process term, describing a multi-step biological "
            "event (e.g., immune response, cell division). Displayed in **teal**."
        ),
        "Cellular Component (pink)": (
            "A GO Cellular Component term describing the location within a cell where a gene "
            "product is active (e.g., nucleus, mitochondria). Displayed in **pink**."
        ),
        "Molecular Function (orange)": (
            "A GO Molecular Function term describing the biochemical activity of a gene product "
            "(e.g., kinase activity, receptor binding). Displayed in **orange**."
        ),
    },

    # ── Edge Types ───────────────────────────────────────────
    "Edge Types (Metaedge Labels)": {
        "CtD — Compound treats Disease": (
            "A known therapeutic relationship indicating that the compound is clinically used "
            "or investigated for treating the disease. These are the **positive labels** in the ML dataset."
        ),
        "CrC — Compound resembles Compound": (
            "Two compounds share significant structural or pharmacological similarity."
        ),
        "CbG — Compound binds Gene": (
            "The compound is known to bind (interact with) the gene product (protein)."
        ),
        "CuG — Compound upregulates Gene": (
            "The compound is known to increase expression of the gene."
        ),
        "CdG — Compound downregulates Gene": (
            "The compound is known to decrease expression of the gene."
        ),
        "DaG — Disease associates with Gene": (
            "The disease has a known genetic association with the gene (e.g., GWAS result)."
        ),
        "DdG — Disease downregulates Gene": (
            "Gene expression is reduced in the context of this disease."
        ),
        "DuG — Disease upregulates Gene": (
            "Gene expression is increased in the context of this disease."
        ),
        "DrD — Disease resembles Disease": (
            "Two diseases share significant phenotypic or molecular similarity."
        ),
        "DlA — Disease localizes in Anatomy": (
            "The disease primarily manifests in or affects this anatomical location."
        ),
        "GiG — Gene interacts with Gene": (
            "A known protein-protein interaction (PPI) between two gene products."
        ),
        "GpBP — Gene participates in Biological Process": (
            "The gene product is involved in a specific GO biological process."
        ),
        "GpCC — Gene participates in Cellular Component": (
            "The gene product is found in a specific cellular location."
        ),
        "GpMF — Gene participates in Molecular Function": (
            "The gene product performs a specific molecular function."
        ),
        "GpPW — Gene participates in Pathway": (
            "The gene product participates in a biological signaling or metabolic pathway."
        ),
        "AeG — Anatomy expresses Gene": (
            "The gene is expressed (active) in this anatomical tissue."
        ),
    },

    # ── ML Model Concepts ────────────────────────────────────
    "Machine Learning Concepts": {
        "Drug Repurposing": (
            "Discovering new therapeutic applications for existing, approved or investigational "
            "drugs. This avoids the cost and time of de novo drug development."
        ),
        "Random Forest": (
            "An ensemble of decision trees. Each tree votes on the predicted class (positive link "
            "vs. negative) and the majority vote wins. Robust to overfitting and handles mixed "
            "feature types well."
        ),
        "Baseline Model": (
            "Random Forest trained on only the four degree features (compound_out_degree, "
            "compound_in_degree, disease_out_degree, disease_in_degree). Serves as a control "
            "to measure how much graph topology improves performance."
        ),
        "Graph (Default) Model": (
            "Random Forest trained on all 13 graph features (degrees + PageRank, Betweenness, "
            "Eigenvector, Clustering, same_louvain_community) with default hyperparameters."
        ),
        "Graph (Fine-Tuned) Model": (
            "The best model — same 13 features but hyperparameters selected via GridSearchCV "
            "(n_estimators=200, max_depth=10, criterion=entropy, etc.). Achieves highest AUC."
        ),
        "Label (0 / 1)": (
            "The training target. 1 = a known drug-disease treatment link (positive). "
            "0 = a drug-disease pair with no known treatment relationship (negative). "
            "Novel drug repurposing candidates are drawn from the negative set."
        ),
        "Predicted Probability / Confidence": (
            "The proportion of decision trees in the forest that voted 'positive' for a given "
            "drug-disease pair. Higher value = stronger model confidence in repurposing potential."
        ),
        "ROC-AUC": (
            "Area Under the ROC Curve. Measures the model's ability to distinguish positives from "
            "negatives across all thresholds. 1.0 = perfect, 0.5 = random."
        ),
        "Precision": (
            "True Positives / (True Positives + False Positives). Of all drug-disease pairs "
            "predicted as repurposing candidates, the fraction that are truly therapeutic."
        ),
        "Recall": (
            "True Positives / (True Positives + False Negatives). Of all true therapeutic pairs, "
            "the fraction correctly identified by the model."
        ),
        "Accuracy": (
            "The fraction of all predictions (positive and negative) that are correct."
        ),
        "Feature Importance": (
            "For Random Forests, the average decrease in Gini impurity contributed by each "
            "feature across all trees. Higher importance = the feature has stronger predictive "
            "signal for distinguishing known from unknown drug-disease links."
        ),
    },

    # ── Distribution Chart ────────────────────────────────────
    "Graph Analytics — Distribution Chart": {
        "X-Axis (metric value)": (
            "The actual value of the selected graph metric (PageRank, Betweenness, etc.) "
            "for nodes in the graph."
        ),
        "Y-Axis (Frequency, Log scale)": (
            "The number of nodes that fall within each value bin. Log scale is used because "
            "graph metrics are typically highly skewed — most nodes have very low values while "
            "a small number of hubs have very high values."
        ),
        "Bar height": (
            "The count of nodes in that metric range. Taller bars = more nodes in that range."
        ),
    },

    # ── Model Comparison Chart ────────────────────────────────
    "Dashboard — Model Comparison Bar Chart": {
        "X-Axis groups (Accuracy, Precision, Recall, ROC-AUC)": (
            "The four performance metrics evaluated on the held-out test set."
        ),
        "Y-Axis range (0.7 – 1.0)": (
            "Cropped range to highlight differences between models. All models score above 70%."
        ),
        "Blue bars — Baseline": "Random Forest with degree features only.",
        "Green bars — Graph (Default)": "Random Forest with all graph features, default settings.",
        "Coral bars — Graph (Fine-Tuned)": "Best model: graph features + optimized hyperparameters.",
    },

    # ── Gauge Chart ──────────────────────────────────────────
    "ML Predictions — Confidence Gauge": {
        "Red zone (0–40%)": "Low confidence. The model does not strongly predict a repurposing link.",
        "Yellow zone (40–70%)": "Moderate confidence. The pair warrants further investigation.",
        "Green zone (70–100%)": "High confidence. Strong predicted repurposing link.",
        "Number (%)": "The predicted probability × 100, i.e. the proportion of trees voting 'positive'.",
    },

    # ── Donut Charts ─────────────────────────────────────────
    "Dashboard — Donut Charts": {
        "Node Types Distribution": (
            "Proportion of each node type (Compound, Disease, Gene, Anatomy, etc.) in the "
            "knowledge graph. Each slice represents a category."
        ),
        "Edge Types Distribution": (
            "Proportion of the top 6 edge relationship types (CbG, CtD, GiG, etc.) in the graph."
        ),
        "Hole (center)": "The donut hole has no meaning — it is a design choice for readability.",
    },

    # ── Ego-Graph Network ─────────────────────────────────────
    "Network Viewer — Ego-Graph Legend": {
        "Central node (largest)": (
            "The node you selected. It is always rendered at the center and slightly larger."
        ),
        "Surrounding nodes": "The immediate 1-hop neighbors of the selected node.",
        "Edge lines": "A known biological or pharmacological relationship between two nodes.",
        "Edge label (metaedge)": "The type of relationship (see Edge Types section above).",
        "Node color": "Indicates the node type — see Node Types section for the color key.",
        "Hover tooltip": "Shows the node name, type (kind), and unique ID.",
    },
}

# ─── Search ───────────────────────────────────────────────────
query = st.text_input("🔍 Search all terms...", "").strip().lower()
st.markdown("---")

# ─── Render by Category ───────────────────────────────────────
any_result = False
for category, terms in TERMS.items():
    matched = {
        term: defn for term, defn in terms.items()
        if not query or query in term.lower() or query in defn.lower()
    }
    if not matched:
        continue
    any_result = True
    st.markdown(f"### {category}")
    for term, defn in matched.items():
        with st.expander(term, expanded=bool(query)):
            st.markdown(defn)
    st.markdown("")

if not any_result:
    st.warning("No terms match your search. Try a shorter or different keyword.")
