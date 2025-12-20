import pandas as pd
import numpy as np
import os
import streamlit as st
from config import CSV_DETAILED, CSV_SUMMARY

@st.cache_data
def load_detailed_data():
    """Load data utama dari CSV dengan path yang aman"""
    try:
        # Cek beberapa lokasi yang mungkin
        possible_paths = [
            CSV_DETAILED,
            "data/march_2025_savings_detailed.csv",
            "march_2025_savings_detailed.csv",
            os.path.join(os.getcwd(), "data", "march_2025_savings_detailed.csv"),
        ]
        
        csv_path = None
        for path in possible_paths:
            if os.path.exists(path):
                csv_path = path
                break
        
        if csv_path is None:
            st.error("❌ File data tidak ditemukan. Pastikan file 'march_2025_savings_detailed.csv' ada di folder 'data/'")
            return pd.DataFrame()
        
        df = pd.read_csv(csv_path)
        
                # Convert timestamp dengan format yang benar
        if 'timestamp' in df.columns:
            # Berdasarkan diagnosa, format Anda adalah: YYYY-MM-DD HH:MM:SS
            df['timestamp'] = pd.to_datetime(
                df['timestamp'], 
                format='%Y-%m-%d %H:%M:%S',
                errors='coerce'
            )
            
            # Cek hasil konversi
            na_count = df['timestamp'].isna().sum()
            if na_count > 0:
                st.warning(f"⚠️ {na_count} timestamp tidak valid")
        
        # Format semua kolom numerik ke 2 desimal
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].round(2)
        
        # Sort by timestamp if available
        if 'timestamp' in df.columns:
            df = df.sort_values('timestamp')
                
        return df
        
    except Exception as e:
        st.error(f"❌ Error memuat data: {str(e)}")
        return pd.DataFrame()


@st.cache_data
def load_summary_data():
    """Load data summary dari CSV"""
    try:
        possible_paths = [
            CSV_SUMMARY,
            "data/march_2025_savings_summary.csv",
            "march_2025_savings_summary.csv",
            os.path.join(os.getcwd(), "data", "march_2025_savings_summary.csv"),
        ]
        
        csv_path = None
        for path in possible_paths:
            if os.path.exists(path):
                csv_path = path
                break
        
        if csv_path is None:
            return None
        
        return pd.read_csv(csv_path)
            
    except Exception as e:
        st.warning(f"⚠️ Tidak bisa load summary data: {str(e)}")
        return None

def get_current_data(df, idx=None):
    """Get current data based on simulation index"""
    if idx is None:
        import streamlit as st
        idx = st.session_state.current_index
    
    if idx < len(df):
        current_idx = min(idx, len(df) - 1)
        return df.iloc[current_idx].copy()
    else:
        return df.iloc[-1].copy()