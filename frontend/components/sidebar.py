import streamlit as st
import requests
import base64
import os

def _load_icon_b64(filename: str) -> str:
    """Load a PNG icon from assets and return base64-encoded data URI."""
    assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
    img_path = os.path.join(assets_dir, filename)
    if os.path.exists(img_path):
        with open(img_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""


def render_sidebar():
    """Render the neon-styled MedGraph sidebar on every page."""
    API_URL = st.secrets.get("API_URL", "http://localhost:8000/api")

    # Pre-load custom icons as base64
    dc_b64 = _load_icon_b64("icon_datacamp.png")
    li_b64 = _load_icon_b64("icon_linkedin.png")

    with st.sidebar:
        # ── 1. Neon Title ──
        st.markdown("""
        <div style="text-align:center; padding: 0.5rem 0 0.2rem 0;">
            <div class="sidebar-neon-title">⚗ MedGraph</div>
            <div class="sidebar-neon-subtitle">BIOMEDICAL GRAPH ANALYTICS</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # ── 2. Page Navigation ──
        st.page_link("About.py", label="About", icon=":material/info:")
        st.page_link("pages/1_Dashboard.py", label="Dashboard", icon=":material/dashboard:")
        st.page_link("pages/2_Graph_Analytics.py", label="Graph Analytics", icon=":material/analytics:")
        st.page_link("pages/3_ML_Predictions.py", label="ML Predictions", icon=":material/model_training:")
        st.page_link("pages/4_Drug_Explorer.py", label="Drug Explorer", icon=":material/travel_explore:")
        st.page_link("pages/5_Network_Viewer.py", label="Network Viewer", icon=":material/hub:")
        st.page_link("pages/6_Terminology.py", label="Terminology", icon=":material/menu_book:")

        st.markdown("---")

        # ── 3. Professional Links with custom generated PNG icons ──
        dc_img = f'<img src="data:image/png;base64,{dc_b64}" class="sidebar-icon-img"/>' if dc_b64 else ""
        li_img = f'<img src="data:image/png;base64,{li_b64}" class="sidebar-icon-img"/>' if li_b64 else ""

        st.markdown(f"""
        <a href="https://datacamp.com/portfolio/afzalsaeed05" target="_blank" class="sidebar-neon-link">
            {dc_img} DataCamp Portfolio
        </a>
        <a href="https://www.linkedin.com/in/afzal-phoenix-soaer/" target="_blank" class="sidebar-neon-link">
            {li_img} LinkedIn Profile
        </a>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # ── 4. Backend Health Status ──
        try:
            health = requests.get(f"{API_URL}/health", timeout=2).json()
            data_ok = health.get("data_loaded", False)
            model_ok = health.get("model_loaded", False)
        except Exception:
            data_ok, model_ok = False, False

        data_cls = "online" if data_ok else "offline"
        model_cls = "online" if model_ok else "offline"

        st.markdown(f"""
        <div style="font-size:0.85rem; color: var(--text-secondary);">
            <span class="health-dot {data_cls}"></span> Data Service<br>
            <span class="health-dot {model_cls}"></span> ML Model
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.caption("BS Data Science · 2026")
