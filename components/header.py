import streamlit as st
from datetime import datetime

def render_header():
    """Render header dashboard"""
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        st.markdown('<h1 class="main-header">⚡ PLN NET PLANT HEAT RATE (NPHR) Optimization Dashboard</h1>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">Sistem Monitoring & Optimisasi Net Plant Heat Rate Pembangkit Listrik - Data Maret 2025</p>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">💡 Data ditampilkan sesuai timestamp yang digunakan untuk optimasi. Beberapa periode tidak tersedia karena data asli memiliki gap; interpolasi hanya untuk perhitungan internal.</p>', unsafe_allow_html=True)
    
    with col2:
        realtime_status = "🟢 LIVE" if st.session_state.simulation_running else "⏸️ PAUSED"
        status_color = "#10B981" if st.session_state.simulation_running else "#F59E0B"
        
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%); 
                    border-radius: 12px; border: 2px solid #E2E8F0;">
            <div style="font-size: 0.9rem; color: #64748B; font-weight: 600;">STATUS SIMULASI</div>
            <div style="font-size: 1.1rem; color: {status_color}; font-weight: 800; margin-top: 0.5rem;">
                {realtime_status}
            </div>
            <div style="font-size: 0.85rem; color: #64748B; margin-top: 0.5rem;">
                {'Running' if st.session_state.simulation_running else 'Paused'}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        current_time = datetime.now()
        refresh_time = current_time.strftime('%H:%M:%S')
        
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #0033A0 0%, #0066CC 100%); 
                    border-radius: 12px; color: white;">
            <div style="font-size: 0.9rem; opacity: 0.9;">UPDATE TERAKHIR</div>
            <div style="font-size: 1.4rem; font-weight: 800; margin-top: 0.5rem;">{refresh_time}</div>
            <div style="font-size: 0.85rem; opacity: 0.9; margin-top: 0.5rem;">{current_time.strftime('%d %b %Y')}</div>
            <div style="font-size: 0.75rem; opacity: 0.8; margin-top: 0.25rem; color: #93C5FD;">
                Refresh: {st.session_state.refresh_interval}s
            </div>
        </div>
        """, unsafe_allow_html=True)