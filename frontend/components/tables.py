import streamlit as st
import pandas as pd

def show_discoveries_table(data_list):
    if not data_list:
        return None
        
    df = pd.DataFrame(data_list)
    df['predicted_probability'] = (df['predicted_probability'] * 100).round(2)
    
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "predicted_probability": st.column_config.ProgressColumn(
                "Confidence (%)",
                help="Prediction confidence",
                format="%f%%",
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
