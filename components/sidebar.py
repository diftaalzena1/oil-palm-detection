import streamlit as st
from utils.formatters import format_number

def render_sidebar(df):
    """Render sidebar dengan control panel"""
    with st.sidebar:
        st.markdown("## ⚙️ **CONTROL PANEL**")
        st.markdown("---")
        
        # Informasi NPHR
        st.markdown("### ℹ️ **Tentang NPHR**")
        st.info("""
        **NPHR (Net Plant Heat Rate)** adalah rasio antara 
        total energi panas yang dikonsumsi dengan energi listrik 
        yang dihasilkan (kcal/kWh). Semakin rendah NPHR, 
        semakin efisien pembangkit.
        """)
        
        st.markdown("---")
        
        # Simulation Controls
        st.markdown("### 🎮 **Kontrol Simulasi**")
        
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            if st.button("▶️ START SIMULASI", type="primary", use_container_width=True):
                st.session_state.simulation_running = True
                st.rerun()
        
        with col_c2:
            if st.button("⏸️ PAUSE", type="secondary", use_container_width=True):
                st.session_state.simulation_running = False
                st.rerun()
        
        # Settings
        
        st.session_state.refresh_interval = st.slider(
            "**Interval Refresh (detik)**",
            min_value=1,
            max_value=10,
            value=3,
            step=1,
            help="Frekuensi update data real-time"
        )
        
        st.markdown("---")
        
        # Data Summary
        st.markdown("### 📊 **Data Summary**")
        
        # Identifikasi parameter
        all_columns = df.columns.tolist()
        lever_params_set = set()
        for col in all_columns:
            if '_now' in col and '_exo_now' not in col:
                from utils.formatters import extract_parameter_base_name
                base_name = extract_parameter_base_name(col)
                lever_params_set.add(base_name)
        
        exo_params = [col for col in all_columns if '_exo_now' in col]
        
        st.markdown(f"""
        - **Total Data Points**: {len(df):,}
        - **Interval Data**: 15 menit
        - **Parameter Lever**: {len(lever_params_set)}
        - **Parameter Exo**: {len(exo_params)}
        """)