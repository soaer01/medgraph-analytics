@echo off
echo Starting MedGraph-Analytics Backend...
start cmd /k "call myenv\Scripts\activate && uvicorn backend.main:app --host 0.0.0.0 --port 8000"

echo Waiting for backend to initialize...
timeout /t 5

echo Starting MedGraph-Analytics Frontend...
start cmd /k "call myenv\Scripts\activate && set PYTHONPATH=%cd% && streamlit run frontend\About.py"

echo Application launched! 
echo Close these windows to stop the servers.
