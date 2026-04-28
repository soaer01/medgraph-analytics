import joblib
import pandas as pd
from backend.config import MODEL_PATH
import os

class MLModel:
    def __init__(self):
        self.model = None
        self.is_loaded = False
        
    def load(self):
        if os.path.exists(MODEL_PATH):
            self.model = joblib.load(MODEL_PATH)
            self.is_loaded = True
            print(f"Model loaded successfully from {MODEL_PATH}")
        else:
            print(f"Warning: Model not found at {MODEL_PATH}")
            
    def predict(self, feature_df: pd.DataFrame):
        if not self.is_loaded:
            raise Exception("Model is not loaded.")
        
        prediction = self.model.predict(feature_df)
        probability = self.model.predict_proba(feature_df)[:, 1]
        
        return prediction[0], probability[0]

# Singleton instance
ml_model_instance = MLModel()
