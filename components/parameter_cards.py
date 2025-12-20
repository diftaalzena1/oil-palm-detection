import streamlit as st
from utils.formatters import get_parameter_unit

def create_parameter_card(param_name, current_val, delta_val, optimized_val, unit=""):
    """Buat kartu untuk parameter lever"""
    delta_color = "value-positive" if delta_val < 0 else "value-negative"
    delta_sign = "+" if delta_val > 0 else ""
    
    # Hitung persentase perubahan
    if current_val != 0:
        pct_change = (delta_val / abs(current_val)) * 100
    else:
        pct_change = 0
    
    # Progress bar width (normalized)
    progress_width = min(100, max(0, abs(pct_change) / 5 * 100))  # Skala 5% = 100%
    
    return f"""
    <div class="pln-param-card">
        <div style="font-size: 0.85rem; color: #64748B; font-weight: 600; margin-bottom: 0.75rem; 
                    display: flex; justify-content: space-between; align-items: center;">
            <span>{param_name}</span>
            <span style="font-size: 0.75rem; color: {'#10B981' if delta_val < 0 else '#D50032'}; 
                      font-weight: 700;">
                {pct_change:+.1f}%
            </span>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="text-align: center;">
                <div style="font-size: 1.1rem; font-weight: 700; color: #0033A0;">
                    {current_val:,.2f}{unit}
                </div>
                <div style="font-size: 0.75rem; color: #64748B; margin-top: 0.25rem;">
                    Sekarang
                </div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 1rem; font-weight: 700;" class="{delta_color}">
                    {delta_sign}{delta_val:,.2f}{unit}
                </div>
                <div style="font-size: 0.75rem; color: #64748B; margin-top: 0.25rem;">
                    Perubahan
                </div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 1.1rem; font-weight: 700; color: #10B981;">
                    {optimized_val:,.2f}{unit}
                </div>
                <div style="font-size: 0.75rem; color: #64748B; margin-top: 0.25rem;">
                    Target
                </div>
            </div>
        </div>
        <div style="margin-top: 1rem; height: 4px; background: #E5E7EB; border-radius: 2px; overflow: hidden;">
            <div style="width: {progress_width}%; height: 100%; 
                      background: linear-gradient(90deg, {'#10B981' if delta_val < 0 else '#D50032'}, 
                      {'#34D399' if delta_val < 0 else '#FF6B6B'});">
            </div>
        </div>
    </div>
    """