import streamlit as st
import plotly.graph_objects as go
from utils.chart_utils import create_gauge_chart
from utils.data_loader import get_current_data

def render_main_dashboard(df):
    """Render tab Dashboard Utama"""
    
    # Get current data
    current_data = get_current_data(df, st.session_state.current_index)
    
    # Create two columns for main charts
    col_chart1, col_chart2 = st.columns([2, 1])
    
    with col_chart1:
        st.markdown('<div class="pln-section-header">📈 TREN NPHR REAL-TIME</div>', unsafe_allow_html=True)
        
        # Get window data
        if st.session_state.current_index >= 1:
            start_idx = max(0, st.session_state.current_index - st.session_state.window_size)
            end_idx = min(st.session_state.current_index + 1, len(df))
            current_df = df.iloc[start_idx:end_idx].copy()
            
            # Buat line chart
            fig = go.Figure()
            
            # Baseline NPHR
            fig.add_trace(go.Scatter(
                x=current_df['timestamp'] if 'timestamp' in current_df.columns else current_df.index,
                y=current_df['baseline_nphr'],
                mode='lines+markers',
                name='Baseline NPHR',
                line=dict(color='#D50032', width=3),
                marker=dict(size=6, color='#D50032'),
                hovertemplate='<b>%{x}</b><br>Baseline: %{y:,.2f} kcal/kWh<extra></extra>'
            ))
            
            # Optimized NPHR
            fig.add_trace(go.Scatter(
                x=current_df['timestamp'] if 'timestamp' in current_df.columns else current_df.index,
                y=current_df['optimized_nphr'],
                mode='lines+markers',
                name='Optimized NPHR',
                line=dict(color='#0033A0', width=3),
                marker=dict(size=6, color='#0033A0'),
                hovertemplate='<b>%{x}</b><br>Optimized: %{y:,.2f} kcal/kWh<extra></extra>'
            ))
            
            # Add current point highlight
            if current_data is not None:
                fig.add_trace(go.Scatter(
                    x=[current_df['timestamp'].iloc[-1] if 'timestamp' in current_df.columns else current_df.index[-1]],
                    y=[current_data['optimized_nphr']],
                    mode='markers',
                    name='Current Point',
                    marker=dict(
                        size=12,
                        color='#10B981',
                        line=dict(width=2, color='white')
                    ),
                    hovertemplate='<b>CURRENT</b><br>Optimized: %{y:,.2f} kcal/kWh<extra></extra>'
                ))
            
            fig.update_layout(
                height=400,
                title="Perkembangan NPHR Real-time",
                xaxis_title="Waktu",
                yaxis_title="NPHR (kcal/kWh)",
                hovermode='x unified',
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                template='plotly_white',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                yaxis=dict(
                    gridcolor='#E5E7EB',
                    zerolinecolor='#E5E7EB'
                ),
                xaxis=dict(
                    gridcolor='#E5E7EB',
                    showgrid=True
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("⏳ Menunggu data real-time...")
    
    with col_chart2:
        st.markdown('<div class="pln-section-header">📊 PERFORMANCE GAUGE</div>', unsafe_allow_html=True)
        
        if current_data is not None:
            # Create gauge chart
            fig = create_gauge_chart(
                current_data.get('optimized_nphr', 0),
                current_data.get('baseline_nphr', 0),
                "Optimized vs Baseline"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Data tidak tersedia untuk gauge chart")