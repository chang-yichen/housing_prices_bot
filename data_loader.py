import pandas as pd
import os
import streamlit as st

@st.cache_data
def load_data(data_folder='ResaleFlatPrices'):
    data_frames = []
    
    for filename in os.listdir(data_folder):
        if filename.endswith('.csv'):
            file_path = os.path.join(data_folder, filename)
            df = pd.read_csv(file_path)
            data_frames.append(df)
    
    # Combine all data into a single DataFrame
    all_data = pd.concat(data_frames, ignore_index=True)
    return all_data