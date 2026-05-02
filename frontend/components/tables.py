import streamlit as st
import pandas as pd

def show_discoveries_table(data_list):
    if not data_list:
        return None
        
    df = pd.DataFrame(data_list)
    df['predicted_probability'] = (df['predicted_probability'] * 100).round(2)
    
    # Reorder columns for better readability
    cols = ['source_name', 'target_name', 'predicted_probability', 'source', 'target']
    # Filter only existing columns
    cols = [c for c in cols if c in df.columns]
    df = df[cols]
    
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "source_name": "Compound Name",
            "target_name": "Disease Name",
            "source": "Compound ID",
            "target": "Disease ID",
            "predicted_probability": st.column_config.ProgressColumn(
                "Confidence (%)",
                help="Prediction confidence",
                format="%.2f%%",
                min_value=0,
                max_value=100,
            )
        }
    )

def show_generic_table(data_list):
    if not data_list:
        return None
    df = pd.DataFrame(data_list)
    st.dataframe(df, use_container_width=True, hide_index=True)
