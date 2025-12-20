import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import os
from utils.data_loader import get_current_data
from utils.formatters import format_currency

def render_impact_analysis(df, summary_df=None):
    """Render tab Impact Analysis"""
    
    st.markdown('<div class="pln-section-header">🏭 IMPACT ANALYSIS</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="pln-info-box">
        <strong>💡 ANALISIS DAMPAK:</strong> Evaluasi menyeluruh manfaat optimasi NPHR dari tiga dimensi:
        1. <strong>Dampak Finansial</strong> - Penghematan biaya & BPP
        2. <strong>Dampak Operasional</strong> - Efisiensi konsumsi batu bara
        3. <strong>Dampak Kinerja</strong> - Peningkatan efisiensi termal
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### DETAILED IMPACT ANALYSIS")
    st.markdown('<span class="real-time-badge">REAL-TIME DATA</span>', unsafe_allow_html=True)
    
    if not df.empty:
        if st.session_state.current_index >= 1:
            start_idx = max(0, st.session_state.current_index - st.session_state.window_size)
            end_idx = min(st.session_state.current_index + 1, len(df))
            savings_df = df.iloc[start_idx:end_idx].copy()

            # GANTI NAMA TAB YANG LEBIH SPESIFIK
            impact_tab1, impact_tab2, impact_tab3, impact_tab4 = st.tabs([
                "💰 Financial Impact",
                "🔥 Operational Impact",
                "⚡ Performance Impact",
                "📊 Summary & Insights"
            ])
            
            with impact_tab1:
                render_financial_impact(savings_df)
            
            with impact_tab2:
                render_operational_impact(savings_df)
            
            with impact_tab3:
                render_performance_impact(savings_df)
            
            with impact_tab4:
                render_summary_insights(savings_df, summary_df)
            
        else:
            st.info("⏳ Menunggu data real-time... Simulasi belum dimulai atau data tidak tersedia.")
    else:
        st.info("⚠️ Data penghematan tidak tersedia.")

def render_financial_impact(savings_df):
    """Render financial impact analysis"""
    st.markdown("### FINANCIAL IMPACT ANALYSIS")
    
    # BAGIAN 1: Penghematan Biaya
    st.markdown("#### 📈 PENGHEMATAN BIAYA BATU BARA")
    
    if 'cost_saving_rp' in savings_df.columns:
        # Hitung metrik kumulatif
        current_interval = savings_df['cost_saving_rp'].iloc[-1] if len(savings_df) > 0 else 0
        total_cumulative = savings_df['cost_saving_rp'].sum()
        avg_per_interval = savings_df['cost_saving_rp'].mean() if len(savings_df) > 0 else 0
        
        col_fin1, col_fin2, col_fin3 = st.columns(3)
        
        with col_fin1:
            st.metric("Interval Terakhir", 
                    f"Rp {current_interval:,.0f}",
                    "15 menit terakhir")
        
        with col_fin2:
            st.metric("Total Kumulatif", 
                    f"Rp {total_cumulative:,.0f}",
                    f"sejak awal pemantauan")
        
        with col_fin3:
            st.metric("Rata-rata per Interval", 
                    f"Rp {avg_per_interval:,.0f}",
                    f"dari {len(savings_df)} interval")
        
        # Grafik penghematan biaya
        fig_cost = go.Figure()
        
        fig_cost.add_trace(go.Scatter(
            x=savings_df['timestamp'] if 'timestamp' in savings_df.columns else savings_df.index,
            y=savings_df['cost_saving_rp'],
            mode='lines+markers',
            name='Penghematan per Interval',
            line=dict(color='#10B981', width=3),
            marker=dict(size=6, color='#10B981'),
            hovertemplate='<b>%{x}</b><br>Penghematan: Rp %{y:,.0f}<extra></extra>'
        ))
        
        fig_cost.update_layout(
            height=400,
            title="Tren Penghematan Biaya Real-time",
            xaxis_title="Waktu",
            yaxis_title="Penghematan Biaya (Rp)",
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
        
        st.plotly_chart(fig_cost, use_container_width=True)

def render_operational_impact(savings_df):
    """Render operational impact analysis"""
    st.markdown("### OPERATIONAL IMPACT ANALYSIS")
    
    # BAGIAN 1: Penghematan Batu Bara
    st.markdown("#### 📊 PENGHEMATAN BATU BARA")
    
    if 'fuel_saving_kg' in savings_df.columns:
        # Statistik dalam kg dan ton
        col_bb1, col_bb2, col_bb3 = st.columns(3)
        
        with col_bb1:
            current_kg = savings_df['fuel_saving_kg'].iloc[-1] if len(savings_df) > 0 else 0
            current_ton = current_kg / 1000
            st.metric("Interval Terakhir",
                    f"{current_ton:.2f} ton",
                    "15 menit terakhir")
        
        with col_bb2:
            total_kg = savings_df['fuel_saving_kg'].sum() if len(savings_df) > 0 else 0
            total_ton = total_kg / 1000
            st.metric("Total Kumulatif",
                    f"{total_ton:.1f} ton",
                    "sejak awal pemantauan")
        
        with col_bb3:
            avg_kg = savings_df['fuel_saving_kg'].mean() if len(savings_df) > 0 else 0
            avg_ton = avg_kg / 1000
            st.metric("Rata-rata per Interval",
                    f"{avg_ton:.3f} ton",
                    f"dari {len(savings_df)} interval")
        
        # Grafik penghematan batu bara
        fig_coal = go.Figure()
        fig_coal.add_trace(go.Scatter(
            x=savings_df['timestamp'] if 'timestamp' in savings_df.columns else savings_df.index,
            y=savings_df['fuel_saving_kg'],
            mode='lines+markers',
            name='Penghematan BB',
            line=dict(color='#F59E0B', width=3),
            marker=dict(size=6, color='#F59E0B'),
            hovertemplate='<b>%{x}</b><br>Penghematan: %{y:,.0f} kg<extra></extra>'
        ))
        
        # Cumulative line dalam ton
        savings_df['cumulative_coal_ton'] = savings_df['fuel_saving_kg'].cumsum() / 1000
        fig_coal.add_trace(go.Scatter(
            x=savings_df['timestamp'] if 'timestamp' in savings_df.columns else savings_df.index,
            y=savings_df['cumulative_coal_ton'],
            mode='lines',
            name='Akumulasi (ton)',
            line=dict(color='#D50032', width=2, dash='dash'),
            yaxis='y2',
            hovertemplate='<b>%{x}</b><br>Akumulasi: %{y:.2f} ton<extra></extra>'
        ))
        
        fig_coal.update_layout(
            height=400,
            title="Tren Penghematan Batu Bara Real-time",
            xaxis_title="Waktu",
            yaxis_title="Penghematan BB (kg)",
            yaxis2=dict(
                title="Akumulasi (ton)",
                overlaying='y',
                side='right'
            ),
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
        
        st.plotly_chart(fig_coal, use_container_width=True)

def render_performance_impact(savings_df):
    """Render performance impact analysis"""
    st.markdown("### PERFORMANCE IMPACT ANALYSIS")
    
    # BAGIAN 1: Efisiensi Trend
    st.markdown("#### 📈 TREN EFISIENSI TERMAL")
    
    if 'efficiency_pct' in savings_df.columns:
        # Grafik efisiensi
        fig_eff = go.Figure()
        fig_eff.add_trace(go.Scatter(
            x=savings_df['timestamp'] if 'timestamp' in savings_df.columns else savings_df.index,
            y=savings_df['efficiency_pct'],
            mode='lines+markers',
            name='Efisiensi',
            line=dict(color='#8B5CF6', width=3),
            marker=dict(size=6, color='#8B5CF6'),
            hovertemplate='<b>%{x}</b><br>Efisiensi: %{y:.2f}%<extra></extra>'
        ))
        
        fig_eff.update_layout(
            height=400,
            title="Tren Efisiensi Real-time",
            xaxis_title="Waktu",
            yaxis_title="Efisiensi (%)",
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
        
        st.plotly_chart(fig_eff, use_container_width=True)
    
    # BAGIAN 2: NPHR Improvement
    st.markdown("---")
    st.markdown("#### 📊 IMPROVEMENT NPHR")

    if 'delta_nphr' in savings_df.columns:
        col_nphr1, col_nphr2, col_nphr3 = st.columns(3)
        
        with col_nphr1:
            current_nphr = savings_df['delta_nphr'].iloc[-1]
            st.metric("Improvement Saat Ini",
                    f"{current_nphr:,.1f}",
                    "kcal/kWh")
        
        with col_nphr2:
            total_nphr = savings_df['delta_nphr'].sum()
            st.metric("Total Improvement",
                    f"{total_nphr:,.1f}",
                    "kcal/kWh")
        
        with col_nphr3:
            avg_nphr = savings_df['delta_nphr'].mean()
            st.metric("Rata-rata Improvement",
                    f"{avg_nphr:,.1f}",
                    "kcal/kWh")

def render_summary_insights(savings_df, summary_df):
    """Render summary and insights"""
    st.markdown("### SUMMARY & INSIGHTS")
    
    # BAGIAN 1: KPI Summary Cards
    st.markdown("#### 📈 OVERALL IMPACT SUMMARY - Maret 2025")
    
    try:
        if summary_df is not None:
            # Ekstrak data dari CSV summary
            total_energy_kwh = summary_df['total_energy_kwh'].iloc[0] if 'total_energy_kwh' in summary_df.columns else 0
            total_fuel_saving_kg = summary_df['total_fuel_saving_kg'].iloc[0] if 'total_fuel_saving_kg' in summary_df.columns else 0
            total_cost_saving_rp = summary_df['total_cost_saving_rp'].iloc[0] if 'total_cost_saving_rp' in summary_df.columns else 0
            avg_efficiency_pct = summary_df['avg_efficiency_pct'].iloc[0] if 'avg_efficiency_pct' in summary_df.columns else 0
            avg_delta_nphr = summary_df['avg_delta_nphr'].iloc[0] if 'avg_delta_nphr' in summary_df.columns else 0
            
            # Tampilkan summary dalam 2 baris
            # Baris 1: Produksi & Penghematan
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="production-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    <div style="font-size: 1rem; font-weight: 600; opacity: 0.9; margin-bottom: 0.5rem;">
                        TOTAL ENERGI DIPRODUKSI
                    </div>
                    <div style="font-size: 2rem; font-weight: 800; margin: 0.5rem 0;">
                        {total_energy_kwh/1e6:,.1f} Juta kWh
                    </div>
                    <div style="font-size: 0.85rem; opacity: 0.9;">
                        Maret 2025
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="coal-saving-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    <div style="font-size: 1rem; font-weight: 600; opacity: 0.9; margin-bottom: 0.5rem;">
                        PENGHEMATAN BATU BARA
                    </div>
                    <div style="font-size: 2rem; font-weight: 800; margin: 0.5rem 0;">
                        {total_fuel_saving_kg/1000:,.1f} ton
                    </div>
                    <div style="font-size: 0.85rem; opacity: 0.9;">
                        {total_fuel_saving_kg:,.0f} kg
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="cost-saving-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    <div style="font-size: 1rem; font-weight: 600; opacity: 0.9; margin-bottom: 0.5rem;">
                        PENGHEMATAN BIAYA
                    </div>
                    <div style="font-size: 2rem; font-weight: 800; margin: 0.5rem 0;">
                        {format_currency(total_cost_saving_rp)}
                    </div>
                    <div style="font-size: 0.85rem; opacity: 0.9;">
                        Total kumulatif
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Baris 2: Efisiensi & Performa
            col4, col5 = st.columns(2)
            
            with col4:
                st.markdown(f"""
                <div class="efficiency-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); color: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    <div style="font-size: 1rem; font-weight: 600; opacity: 0.9; margin-bottom: 0.5rem;">
                        PENINGKATAN EFISIENSI
                    </div>
                    <div style="font-size: 2rem; font-weight: 800; margin: 0.5rem 0;">
                        +{avg_efficiency_pct:.2f}%
                    </div>
                    <div style="font-size: 0.85rem; opacity: 0.9;">
                        Rata-rata per interval
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col5:
                st.markdown(f"""
                <div class="nphr-card" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); color: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    <div style="font-size: 1rem; font-weight: 600; opacity: 0.9; margin-bottom: 0.5rem;">
                        PENURUNAN NPHR
                    </div>
                    <div style="font-size: 2rem; font-weight: 800; margin: 0.5rem 0;">
                        {avg_delta_nphr:.1f} kcal/kWh
                    </div>
                    <div style="font-size: 0.85rem; opacity: 0.9;">
                        Peningkatan efisiensi
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
        else:
            # Fallback jika file summary tidak ditemukan
            st.warning("File summary tidak ditemukan. Menggunakan data real-time...")
            
            # Hitung dari savings_df sebagai fallback
            total_cost_saving = savings_df['cost_saving_rp'].sum() if 'cost_saving_rp' in savings_df.columns else 0
            total_coal_saving = savings_df['fuel_saving_kg'].sum() if 'fuel_saving_kg' in savings_df.columns else 0
            avg_efficiency = savings_df['efficiency_pct'].mean() if 'efficiency_pct' in savings_df.columns else 0
            avg_improvement = savings_df['delta_nphr'].mean() if 'delta_nphr' in savings_df.columns else 0
            
            # Tampilkan fallback dengan 4 metrik saja
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    <div style="font-size: 1rem; font-weight: 600; opacity: 0.9; margin-bottom: 0.5rem;">
                        PENGHEMATAN BIAYA
                    </div>
                    <div style="font-size: 2rem; font-weight: 800; margin: 0.5rem 0;">
                        {format_currency(total_cost_saving)}
                    </div>
                    <div style="font-size: 0.85rem; opacity: 0.9;">
                        Data real-time
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    <div style="font-size: 1rem; font-weight: 600; opacity: 0.9; margin-bottom: 0.5rem;">
                        PENGHEMATAN BATU BARA
                    </div>
                    <div style="font-size: 2rem; font-weight: 800; margin: 0.5rem 0;">
                        {total_coal_saving/1000:,.1f} ton
                    </div>
                    <div style="font-size: 0.85rem; opacity: 0.9;">
                        {total_coal_saving:,.0f} kg
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); color: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    <div style="font-size: 1rem; font-weight: 600; opacity: 0.9; margin-bottom: 0.5rem;">
                        EFISIENSI
                    </div>
                    <div style="font-size: 2rem; font-weight: 800; margin: 0.5rem 0;">
                        {avg_efficiency:.2f}%
                    </div>
                    <div style="font-size: 0.85rem; opacity: 0.9;">
                        Peningkatan
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); color: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    <div style="font-size: 1rem; font-weight: 600; opacity: 0.9; margin-bottom: 0.5rem;">
                        IMPROVEMENT NPHR
                    </div>
                    <div style="font-size: 2rem; font-weight: 800; margin: 0.5rem 0;">
                        {avg_improvement:.1f}
                    </div>
                    <div style="font-size: 0.85rem; opacity: 0.9;">
                        kcal/kWh
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
        st.info("Silakan periksa koneksi data atau file summary.")