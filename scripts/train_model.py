import pandas as pd
import numpy as np
import json
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score

def train_and_save_model():
    print("Loading datasets...")
    # Get absolute paths to data
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ml_dataset_path = os.path.join(base_dir, 'baseline_ml_dataset.csv')
    graph_metrics_path = os.path.join(base_dir, 'graph_metrics.csv')
    
    ml_dataset = pd.read_csv(ml_dataset_path)
    graph_metrics = pd.read_csv(graph_metrics_path)

    print("Merging graph metrics...")
    ml_dataset = ml_dataset.merge(graph_metrics, left_on='source', right_on='id', how='left').rename(columns={
        'pagerank': 'compound_pagerank', 'betweenness': 'compound_betweenness',
        'eigenvector': 'compound_eigenvector', 'louvain': 'compound_louvain',
        'lpa': 'compound_lpa', 'clustering': 'compound_clustering'
    }).drop(columns=['id'])

    ml_dataset = ml_dataset.merge(graph_metrics, left_on='target', right_on='id', how='left').rename(columns={
        'pagerank': 'disease_pagerank', 'betweenness': 'disease_betweenness',
        'eigenvector': 'disease_eigenvector', 'louvain': 'disease_louvain',
        'lpa': 'disease_lpa', 'clustering': 'disease_clustering'
    }).drop(columns=['id'])

    ml_dataset['same_louvain_community'] = (ml_dataset['compound_louvain'] == ml_dataset['disease_louvain']).astype(int)
    ml_dataset.fillna(0, inplace=True)

    y = ml_dataset['label']

    baseline_features = ['compound_out_degree', 'compound_in_degree', 'disease_out_degree', 'disease_in_degree']
    X_baseline = ml_dataset[baseline_features]

    graph_features = baseline_features + [
        'compound_pagerank', 'disease_pagerank', 'compound_betweenness', 'disease_betweenness',
        'compound_eigenvector', 'disease_eigenvector', 'compound_clustering', 'disease_clustering',
        'same_louvain_community'
    ]
    X_graph = ml_dataset[graph_features]

    print("Splitting datasets...")
    X_base_train, X_base_test, y_train, y_test = train_test_split(X_baseline, y, test_size=0.2, random_state=42)
    X_graph_train, X_graph_test, _, _ = train_test_split(X_graph, y, test_size=0.2, random_state=42)

    print("Training Baseline Model...")
    rf_baseline = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    rf_baseline.fit(X_base_train, y_train)
    base_preds = rf_baseline.predict(X_base_test)
    base_probs = rf_baseline.predict_proba(X_base_test)[:, 1]

    print("Training Graph (Default) Model...")
    rf_graph = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    rf_graph.fit(X_graph_train, y_train)
    graph_preds = rf_graph.predict(X_graph_test)
    graph_probs = rf_graph.predict_proba(X_graph_test)[:, 1]

    print("Training Graph (Fine-Tuned) Model with optimal parameters...")
    # Best params from GridSearchCV in the notebook
    best_params = {
        'bootstrap': True, 'criterion': 'entropy', 'max_depth': 10, 
        'max_features': 'sqrt', 'min_samples_leaf': 1, 'min_samples_split': 10, 'n_estimators': 200
    }
    best_rf_model = RandomForestClassifier(random_state=42, n_jobs=-1, **best_params)
    best_rf_model.fit(X_graph_train, y_train)
    
    tuned_preds = best_rf_model.predict(X_graph_test)
    tuned_probs = best_rf_model.predict_proba(X_graph_test)[:, 1]

    print("Calculating metrics...")
    metrics_data = {
        'Model': ['Baseline', 'Baseline', 'Baseline', 'Baseline',
                  'Graph (Default)', 'Graph (Default)', 'Graph (Default)', 'Graph (Default)',
                  'Graph (Fine-Tuned)', 'Graph (Fine-Tuned)', 'Graph (Fine-Tuned)', 'Graph (Fine-Tuned)'],
        'Metric': ['Accuracy', 'Precision', 'Recall', 'ROC-AUC'] * 3,
        'Score': [
            accuracy_score(y_test, base_preds), precision_score(y_test, base_preds), recall_score(y_test, base_preds), roc_auc_score(y_test, base_probs),
            accuracy_score(y_test, graph_preds), precision_score(y_test, graph_preds), recall_score(y_test, graph_preds), roc_auc_score(y_test, graph_probs),
            accuracy_score(y_test, tuned_preds), precision_score(y_test, tuned_preds), recall_score(y_test, tuned_preds), roc_auc_score(y_test, tuned_probs)
        ]
    }
    
    metrics_df = pd.DataFrame(metrics_data)
    
    # Extract feature importances
    importances = best_rf_model.feature_importances_
    feature_names = list(X_graph.columns)
    
    importance_list = []
    for feat, imp in zip(feature_names, importances):
        importance_list.append({"feature": feat, "importance_score": float(imp)})
    
    # Sort importances
    importance_list = sorted(importance_list, key=lambda x: x['importance_score'], reverse=True)

    print("Saving models and metrics...")
    # Create backend/data directory
    data_dir = os.path.join(base_dir, 'backend', 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    model_path = os.path.join(data_dir, 'trained_model.joblib')
    joblib.dump(best_rf_model, model_path)
    
    metrics_path = os.path.join(data_dir, 'model_metrics.json')
    with open(metrics_path, 'w') as f:
        json.dump({
            "metrics": metrics_data,
            "feature_importance": importance_list,
            "features": feature_names
        }, f, indent=4)
        
    print(f"Success! Model saved to {model_path}")
    print(f"Metrics saved to {metrics_path}")

if __name__ == "__main__":
    train_and_save_model()
