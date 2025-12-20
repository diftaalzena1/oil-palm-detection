import streamlit as st
import pandas as pd
from utils.formatters import format_number
from utils.data_loader import get_current_data
from datetime import datetime, timedelta

def render_kpi_section(df):
    """Render KPI metrics section"""
    st.markdown("## 📊 **PERFORMANCE METRICS**")
    st.markdown('<span class="real-time-badge">REAL-TIME</span>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Get current data
    current_data = get_current_data(df, st.session_state.current_index)
    
    # Create metrics grid
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Metric 1: NPHR Baseline
        if 'baseline_nphr' in current_data:
            baseline_val = current_data['baseline_nphr']
            avg_baseline = df['baseline_nphr'].mean() if len(df) > 0 else baseline_val
            
            st.markdown(f"""
            <div class="pln-metric-card">
                <div class="pln-metric-label">NPHR BASELINE</div>
                <div class="pln-metric-value">{format_number(baseline_val)}</div>
                <div style="font-size: 0.85rem; color: #64748B; margin-top: 0.5rem;">
                    vs Rata-rata: <span style="color: {'#D50032' if baseline_val > avg_baseline else '#10B981'}; 
                    font-weight: 600;">{(baseline_val - avg_baseline):+.2f}</span> kcal/kWh
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        # Metric 2: NPHR Optimized
        if 'optimized_nphr' in current_data:
            optimized_val = current_data['optimized_nphr']
            avg_optimized = df['optimized_nphr'].mean() if len(df) > 0 else optimized_val
            
            st.markdown(f"""
            <div class="pln-metric-card">
                <div class="pln-metric-label">NPHR OPTIMIZED</div>
                <div class="pln-metric-value">{format_number(optimized_val)}</div>
                <div style="font-size: 0.85rem; color: #64748B; margin-top: 0.5rem;">
                    vs Rata-rata: <span style="color: {'#D50032' if optimized_val > avg_optimized else '#10B981'}; 
                    font-weight: 600;">{(optimized_val - avg_optimized):+.2f}</span> kcal/kWh
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
        # Metric 3: Penghematan NPHR
        if 'delta_nphr' in current_data:
            delta_val = current_data['delta_nphr']
            baseline_val = current_data.get('baseline_nphr', 0)
            optimized_val = current_data.get('optimized_nphr', 0)
            improvement_pct = ((baseline_val - optimized_val) / baseline_val * 100) if baseline_val != 0 else 0
            
            improvement_class = "pln-improvement-positive" if delta_val > 0 else "pln-improvement-negative"
            
            st.markdown(f"""
            <div class="pln-metric-card">
                <div class="pln-metric-label">PENGHEMATAN NPHR</div>
                <div class="pln-metric-value {improvement_class}">{format_number(delta_val)}</div>
                <div style="font-size: 0.85rem; color: #64748B; margin-top: 0.5rem;">
                    <span class="{improvement_class}">{improvement_pct:+.2f}%</span> lebih efisien
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col4:
        # Metric 4: Timestamp dari Data Saat Ini (Sama Tinggi dengan Metric 3)
        if current_data is not None:
            # Cek kolom timestamp yang tersedia
            timestamp = None
            
            # Cari kolom yang mengandung 'timestamp' (case insensitive)
            timestamp_cols = [col for col in current_data.index if 'timestamp' in col.lower() or 'date' in col.lower() or 'time' in col.lower()]
            
            if timestamp_cols:
                timestamp = current_data[timestamp_cols[0]]
            else:
                # Jika tidak ada, gunakan index
                timestamp = f"Data Point {st.session_state.current_index + 1}"
            
            if timestamp is not None:
                try:
                    # Konversi ke datetime jika belum
                    if isinstance(timestamp, (datetime, pd.Timestamp)):
                        # Format tanggal dan waktu
                        date_time_str = timestamp.strftime('%d/%m %H:%M')
                        date_str = timestamp.strftime('%d %b %Y')
                    elif isinstance(timestamp, str):
                        # Jika string, coba parse
                        try:
                            ts = pd.to_datetime(timestamp)
                            date_time_str = ts.strftime('%d/%m %H:%M')
                            date_str = ts.strftime('%d %b %Y')
                        except:
                            date_time_str = str(timestamp)[:16]
                            date_str = str(timestamp)[:10]
                    else:
                        date_time_str = str(timestamp)[:16]
                        date_str = "N/A"
                    
                    st.markdown(f"""
                    <div class="pln-metric-card">
                        <div class="pln-metric-label">TIMESTAMP DATA</div>
                        <div class="pln-metric-value" style="font-size: 1.8rem; color: #D50032; margin-top: 0.5rem;">
                            {date_time_str}
                        </div>
                        <div style="font-size: 0.85rem; color: #64748B; margin-top: 0.5rem;">
                            {date_str} • Point {st.session_state.current_index + 1}/{len(df)}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                except Exception as e:
                    # Fallback jika gagal parsing
                    st.markdown(f"""
                    <div class="pln-metric-card">
                        <div class="pln-metric-label">TIMESTAMP DATA</div>
                        <div class="pln-metric-value" style="font-size: 1.8rem; color: #D50032; margin-top: 0.5rem;">
                            Point {st.session_state.current_index + 1}
                        </div>
                        <div style="font-size: 0.85rem; color: #64748B; margin-top: 0.5rem;">
                            dari {len(df)} total • Error: {str(e)[:30]}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                # Jika tidak ada timestamp
                st.markdown(f"""
                <div class="pln-metric-card">
                    <div class="pln-metric-label">DATA POINT</div>
                    <div class="pln-metric-value" style="font-size: 1.8rem; margin-top: 0.5rem;">
                        {st.session_state.current_index + 1}
                    </div>
                    <div style="font-size: 0.85rem; color: #64748B; margin-top: 0.5rem;">
                        dari {len(df)} total
                    </div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")