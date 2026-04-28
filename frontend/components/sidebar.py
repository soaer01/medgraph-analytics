import streamlit as st
import requests

def render_sidebar():
    API_URL = st.secrets.get("API_URL", "http://localhost:8000/api")
    
    with st.sidebar:
        # 1. Title Section
        st.markdown("## :material/science: MedGraph")
        st.caption("Biomedical Graph Analytics & ML")
        st.markdown("---")

        # 2. Page Navigation Menu
        st.page_link("About.py", label="About", icon=":material/info:")
        st.page_link("pages/1_Dashboard.py", label="Dashboard", icon=":material/dashboard:")
        st.page_link("pages/2_Graph_Analytics.py", label="Graph Analytics", icon=":material/analytics:")
        st.page_link("pages/3_ML_Predictions.py", label="ML Predictions", icon=":material/model_training:")
        st.page_link("pages/4_Drug_Explorer.py", label="Drug Explorer", icon=":material/travel_explore:")
        st.page_link("pages/5_Network_Viewer.py", label="Network Viewer", icon=":material/hub:")
        st.page_link("pages/6_Terminology.py", label="Terminology", icon=":material/menu_book:")
        
        st.markdown("---")

        # 3. Professional Links
        st.markdown("💼 [Datacamp Portfolio](https://datacamp.com/portfolio/afzalsaeed05)")
        st.markdown("🔗 [LinkedIn Profile](https://www.linkedin.com/in/afzal-phoenix-soaer/)")
        
        st.markdown("---")

        # 4. Backend Health Status
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
