import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from utils.data_loader import get_current_data
from utils.formatters import extract_parameter_base_name

def render_exogenous_params(df):
    """Render tab Parameter Exogenous"""
    
    st.markdown('<div class="pln-section-header">🌡️ MONITORING PARAMETER EXOGENOUS REAL-TIME</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="pln-info-box">
        <strong>💡 INFORMASI:</strong> Parameter Exogenous adalah variabel eksternal yang tidak dapat 
        dikontrol namun mempengaruhi performa pembangkit. Parameter ini digunakan sebagai input 
        untuk model optimasi.
    </div>
    """, unsafe_allow_html=True)
    
    # Identifikasi parameter exo
    all_columns = df.columns.tolist()
    exo_columns = [col for col in all_columns if '_exo_now' in col]
    
    # Get current data
    current_data = get_current_data(df, st.session_state.current_index)
    
    if exo_columns:
        # Header dengan status real-time
        col_header1, col_header2 = st.columns([3, 1])
        with col_header1:
            st.markdown("### 📊 PARAMETER EXOGENOUS REAL-TIME")
        with col_header2:
            st.markdown(f'<span class="real-time-badge">LIVE UPDATE</span>', unsafe_allow_html=True)
        
        # Tampilkan parameter exo dalam grid real-time
        cols = st.columns(3)
        for idx, exo_col in enumerate(exo_columns):
            with cols[idx % 3]:
                if current_data is not None and exo_col in df.columns:
                    value = current_data[exo_col]
                    param_name = exo_col.replace('_exo_now', '')
                    
                    # Hitung statistik dari window data saat ini
                    if st.session_state.current_index >= 1:
                        start_idx = max(0, st.session_state.current_index - st.session_state.window_size)
                        end_idx = min(st.session_state.current_index + 1, len(df))
                        window_data = df.iloc[start_idx:end_idx].copy()
                        
                        if exo_col in window_data.columns:
                            min_val = window_data[exo_col].min()
                            max_val = window_data[exo_col].max()
                            mean_val = window_data[exo_col].mean()
                            
                            # Hitung perubahan dari data sebelumnya
                            if st.session_state.current_index > 0:
                                prev_val = df.iloc[st.session_state.current_index - 1][exo_col]
                                change = value - prev_val
                                change_pct = (change / prev_val * 100) if prev_val != 0 else 0
                                change_sign = "+" if change > 0 else ""
                                change_color = "#10B981" if change < 0 else "#D50032"
                            else:
                                change = 0
                                change_pct = 0
                                change_sign = ""
                                change_color = "#64748B"
                    else:
                        min_val = df[exo_col].min()
                        max_val = df[exo_col].max()
                        mean_val = df[exo_col].mean()
                        change = 0
                        change_pct = 0
                        change_sign = ""
                        change_color = "#64748B"
                    
                    st.markdown(f"""
                    <div class="pln-param-card" style="border-left: 4px solid {change_color};">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                            <div style="font-size: 0.85rem; color: #64748B; font-weight: 600;">
                                {param_name}
                            </div>
                            <div style="font-size: 0.75rem; color: {change_color}; font-weight: 700;">
                                {change_sign}{change:+.2f}
                            </div>
                        </div>
                        <div style="font-size: 1.3rem; font-weight: 800; color: #0033A0; margin: 0.5rem 0;">
                            {value:,.2f}
                        </div>
                        <div style="font-size: 0.75rem; color: #64748B;">
                            <div style="display: flex; justify-content: space-between;">
                                <span>Rata: {mean_val:,.2f}</span>
                                <span>{change_pct:+.1f}%</span>
                            </div>
                            <div style="margin-top: 0.25rem; display: flex; justify-content: space-between;">
                                <span>Min: {min_val:,.2f}</span>
                                <span>Max: {max_val:,.2f}</span>
                            </div>
                        </div>
                        <div style="margin-top: 0.5rem; height: 4px; background: #E5E7EB; border-radius: 2px; overflow: hidden;">
                            <div style="width: {((value - min_val) / (max_val - min_val) * 100) if max_val != min_val else 50}%; 
                                      height: 100%; background: linear-gradient(90deg, #8B5CF6, #A78BFA);">
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Tren parameter exo real-time
        st.markdown("---")
        st.markdown("### 📈 TREN PARAMETER EXOGENOUS REAL-TIME")
        
        # Kontrol untuk grafik
        col_control1, col_control2, col_control3 = st.columns([2, 1, 1])
        
        with col_control1:
            # Pilih parameter untuk ditampilkan tren
            selected_exo = st.selectbox(
                "Pilih Parameter untuk Tren Real-time",
                options=[col.replace('_exo_now', '') for col in exo_columns],
                key="exo_param_select"
            )
        
        with col_control2:
            # Pilih window size untuk grafik
            exo_window_size = st.selectbox(
                "Rentang Data",
                options=[10, 20, 30, 50, 100],
                index=1,
                key="exo_window_size"
            )
        
        with col_control3:
            # Pilih tipe grafik
            chart_type = st.radio(
                "Tipe Grafik",
                ["Line", "Area"],
                horizontal=True,
                key="exo_chart_type"
            )
        
        if selected_exo and st.session_state.current_index >= 1:
            exo_col = f"{selected_exo}_exo_now"
            if exo_col in df.columns:
                # Prepare real-time data
                start_idx = max(0, st.session_state.current_index - exo_window_size)
                end_idx = min(st.session_state.current_index + 1, len(df))
                trend_data = df.iloc[start_idx:end_idx].copy()
                
                fig = go.Figure()
                
                if chart_type == "Line":
                    fig.add_trace(go.Scatter(
                        x=trend_data['timestamp'] if 'timestamp' in trend_data.columns else trend_data.index,
                        y=trend_data[exo_col],
                        mode='lines+markers',
                        name=selected_exo,
                        line=dict(color='#8B5CF6', width=3),
                        marker=dict(size=6, color='#8B5CF6'),
                        hovertemplate='<b>%{x}</b><br>' +
                                    f'{selected_exo}: %{{y:,.2f}}<extra></extra>',
                        fill=None
                    ))
                else:
                    fig.add_trace(go.Scatter(
                        x=trend_data['timestamp'] if 'timestamp' in trend_data.columns else trend_data.index,
                        y=trend_data[exo_col],
                        mode='lines',
                        name=selected_exo,
                        line=dict(color='#8B5CF6', width=3),
                        fill='tozeroy',
                        fillcolor='rgba(139, 92, 246, 0.2)',
                        hovertemplate='<b>%{x}</b><br>' +
                                    f'{selected_exo}: %{{y:,.2f}}<extra></extra>'
                    ))
                
                # Add current point highlight
                if current_data is not None and exo_col in current_data:
                    current_time = trend_data['timestamp'].iloc[-1] if 'timestamp' in trend_data.columns else trend_data.index[-1]
                    
                    fig.add_trace(go.Scatter(
                        x=[current_time],
                        y=[current_data[exo_col]],
                        mode='markers+text',
                        name='Current Value',
                        marker=dict(
                            size=15,
                            color='#10B981',
                            line=dict(width=3, color='white'),
                            symbol='diamond'
                        ),
                        text=[f"{current_data[exo_col]:,.2f}"],
                        textposition="top center",
                        textfont=dict(size=12, color='#0033A0', family="Arial Black"),
                        hovertemplate='<b>CURRENT</b><br>' +
                                    f'{selected_exo}: %{{y:,.2f}}<extra></extra>'
                    ))
                
                fig.update_layout(
                    height=450,
                    title=f"Tren Real-time: {selected_exo}",
                    xaxis_title="Waktu",
                    yaxis_title=f"Nilai {selected_exo}",
                    hovermode='x unified',
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                    ),
                    template='plotly_white'
                )
                
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("⚠️ Tidak ada parameter exogenous yang ditemukan dalam dataset.")