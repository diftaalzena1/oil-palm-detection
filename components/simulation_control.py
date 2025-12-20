import streamlit as st
import time
from utils.formatters import format_currency

def render_simulation_control(df):
    """Render simulation control section"""
    st.markdown("---")
    st.markdown("## **CONTROL**")
    
    if st.session_state.simulation_running and st.session_state.current_index < len(df):
        # Show simulation status
        status_col1, status_col2, status_col3 = st.columns(3)
        
        with status_col1:
            st.info(f"**🔄 Processing:** Data ke-{st.session_state.current_index + 1} dari {len(df)}")
        
        with status_col2:
            st.info(f"**⏱️ Next Update:** {st.session_state.refresh_interval} detik")
        
        with status_col3:
            if st.button("⏸️ PAUSE SIMULATION", type="secondary"):
                st.session_state.simulation_running = False
                st.rerun()
        
        # Update progress
        time.sleep(st.session_state.refresh_interval)
        st.session_state.current_index = min(st.session_state.current_index + 1, len(df))
        st.rerun()
    
    elif st.session_state.current_index >= len(df):
        # Simulation completed
        st.balloons()
        
        col_comp1, col_comp2 = st.columns([3, 1])
        with col_comp1:
            st.success("""
            ## 🎉 **SIMULASI SELESAI!**
            
            Semua data telah diproses. Berikut ringkasan hasil:
            """)
            
            # Tampilkan ringkasan akhir
            if not df.empty:
                total_cost = df['cost_saving_rp'].sum() if 'cost_saving_rp' in df.columns else 0
                total_coal = df['fuel_saving_kg'].sum() if 'fuel_saving_kg' in df.columns else 0
                
                st.markdown(f"""
                ### 📊 Hasil Akhir:
                - **Total Penghematan Biaya**: {format_currency(total_cost)}
                - **Total Penghematan Batu Bara**: {total_coal/1000:,.1f} ton
                - **Rata-rata Efisiensi**: {df['efficiency_pct'].mean():.2f}% (jika tersedia)
                - **Rata-rata Improvement NPHR**: {df['delta_nphr'].mean():,.1f} kcal/kWh
                - **Total Data Points Diproses**: {len(df):,}
                """)
        
        with col_comp2:
            if st.button("🔄 RESTART SIMULATION", type="primary"):
                st.session_state.current_index = 0
                st.session_state.simulation_running = True
                st.rerun()