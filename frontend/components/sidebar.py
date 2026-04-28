import streamlit as st
import requests

def render_sidebar():
    API_URL = st.secrets.get("API_URL", "http://localhost:8000/api")
    
    with st.sidebar:
        st.markdown("## 🧬 MedGraph")
        st.caption("Biomedical Graph Analytics & ML")
        st.markdown("---")

        # Live backend health check
        try:
            health = requests.get(f"{API_URL}/health", timeout=2).json()
            data_ok = "🟢" if health.get("data_loaded") else "🔴"
            model_ok = "🟢" if health.get("model_loaded") else "🔴"
        except Exception:
            data_ok, model_ok = "🔴", "🔴"

        st.markdown(f"**Data Service** {data_ok}")
        st.markdown(f"**ML Model** {model_ok}")
        st.markdown("---")
        st.caption("BS Data Science · 2026")
