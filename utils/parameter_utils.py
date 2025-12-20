import streamlit as st
import pandas as pd

def get_parameter_value(current_data, param_name, suffix_type):
    """
    Get parameter value dengan berbagai kemungkinan format
    
    Parameters:
    - current_data: Series atau dict dengan data saat ini
    - param_name: Nama parameter dasar (tanpa suffix)
    - suffix_type: '_now', '_delta', atau '_optimized'
    """
    # Coba berbagai format yang mungkin
    possible_names = [
        f"{param_name}_lever{suffix_type}",  # Format dataset Anda
        f"{param_name}{suffix_type}",        # Format alternatif
        param_name                            # Coba tanpa suffix
    ]
    
    for name in possible_names:
        if name in current_data:
            value = current_data[name]
            # Konversi ke float jika perlu
            try:
                return float(value)
            except:
                return value
    
    return None

def check_parameter_exists(df, param_name):
    """
    Cek apakah parameter ada dalam dataset dengan berbagai format
    """
    suffixes = ['_lever_now', '_lever_delta', '_lever_optimized']
    
    for suffix in suffixes:
        col_name = f"{param_name}{suffix}"
        if col_name in df.columns:
            return True
    
    return False

def get_available_parameters(df):
    """
    Get semua parameter lever yang tersedia dalam dataset
    """
    lever_params = set()
    
    for col in df.columns:
        if '_lever_now' in col:
            # Ekstrak nama dasar
            base_name = col.replace('_lever_now', '')
            lever_params.add(base_name)
    
    return sorted(list(lever_params))