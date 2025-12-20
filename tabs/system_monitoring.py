import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from utils.model_mapping import create_model_mapping
from utils.formatters import extract_parameter_base_name, get_parameter_unit
from utils.data_loader import get_current_data
from components.parameter_cards import create_parameter_card

def render_system_monitoring(df):
    """Render tab Monitoring Sistem Pembangkit"""
    
    st.markdown('<div class="pln-section-header">🔧 MONITORING SISTEM PEMBANGKIT</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="pln-info-box">
        <strong>💡 INFORMASI:</strong> Setiap sistem pembangkit memiliki parameter operasional yang dapat dioptimasi 
        untuk meningkatkan efisiensi. Monitor parameter ini untuk mencapai NPHR yang optimal.
    </div>
    """, unsafe_allow_html=True)
    
    # Import fungsi helper baru
    from utils.parameter_utils import get_parameter_value, check_parameter_exists, get_available_parameters
    
    # Get current data
    current_data = get_current_data(df, st.session_state.current_index)
    
    # DEBUG: Tampilkan parameter yang tersedia
    with st.sidebar.expander("🔍 DEBUG - Parameter Tersedia"):
        available_params = get_available_parameters(df)
        st.write(f"Total parameter: {len(available_params)}")
        st.write("Contoh parameter:", available_params[:10])
    
    # Update model mapping
    model_mapping_updated = {
        'BOILER': {
            'icon': '🔥',
            'name': 'BOILER SYSTEM',
            'params': [
                'No1 AIR PH INLET FLUE GAS O2',
                'No2 AIR PH INLET FLUE GAS O2',
                'COAL FLOW MILL GROUP 1 P',
                'No.1 FD FAN MOVABLE BLADE POSI',
                'No.2 FD FAN MOVABLE BLADE POSI',
                'BURNOUT AIR DOWN ANGLE 1 SEC AIR VLV POST',
                'BURNOUT AIR MIDDLE ANGLE 1 SEC AIR VLV POST',
                'BURNOUT AIR UP ANGLE 1 SEC AIR VLV POST'
            ],
            'color': '#D50032',
            'description': 'Sistem boiler dan pembakaran'
        },
        'SPRAY1': {
            'icon': '💦',
            'name': 'SPRAY 1 SYSTEM',
            'params': [
                'R SH 1ST SPRAY WATER FLOW',
                'L SH 1ST SPRAY WATER FLOW',
                'SH 1ST SPRAY OUT STM TEMP R',
                'SH 1ST SPRAY IN STM TEMP(R)',
                'SH 1ST SPRAY IN STM TEMP(L)'
            ],
            'color': '#0066CC',
            'description': 'Sistem spray pertama'
        },
        'SPRAY2': {
            'icon': '🌊',
            'name': 'SPRAY 2 SYSTEM',
            'params': [
                'L SH 2ST SPRAY WATER FLOW',
                'R SH 2ST SPRAY WATER FLOW',
                'SH 2ND SPRAY OUT STM TEMP L',
                'SH 2ND SPRAY OUT STM TEMP R'
            ],
            'color': '#0096FF',
            'description': 'Sistem spray kedua'
        },
        'HPH': {
            'icon': '📊',
            'name': 'HIGH PRESSURE HEATER',
            'params': [
                'NO.1 HP HEATER LVL',
                'NO.3 HP HEATER LVL',
                'NO.2 HP HEATER LVL',
                'HP HEATER OUTLET HDR WTR TEMP'
            ],
            'color': '#10B981',
            'description': 'Pemanas tekanan tinggi'
        },
        'STEAM': {
            'icon': '💨',
            'name': 'STEAM SYSTEM',
            'params': [
                'MAIN STEAM OUTLET TEMPERATURE',
                'MAIN STEAM PRESSURE',
                'CDST A SIDE WTR CIRCLE INLET PRESS',
                'CDST B SIDE WTR CIRCLE INLET PRESS'
            ],
            'color': '#8B5CF6',
            'description': 'Sistem steam utama'
        }
    }
    
    # Buat parameter mapping yang valid berdasarkan dataset
    valid_model_mapping = {}
    
    for model_key, model_info in model_mapping_updated.items():
        valid_params = []
        for param in model_info['params']:
            if check_parameter_exists(df, param):
                valid_params.append(param)
        
        if valid_params:
            valid_model_mapping[model_key] = {
                'icon': model_info['icon'],
                'name': model_info['name'],
                'params': valid_params,
                'color': model_info['color'],
                'description': model_info['description']
            }
    
    # Tampilkan pilihan sistem
    st.markdown("### 🔍 Pilih Sistem untuk Dimonitor")
    
    # Buat list sistem yang tersedia
    available_systems = []
    for model_key, model_info in valid_model_mapping.items():
        display_name = f"{model_info['icon']} {model_info['name']}"
        param_count = len(model_info['params'])
        available_systems.append({
            'key': model_key,
            'display': f"{display_name} ({param_count} parameter)",
            'info': model_info
        })
    
    if not available_systems:
        st.warning("⚠️ Tidak ada sistem yang ditemukan dalam dataset.")
        with st.expander("📋 Lihat semua parameter yang tersedia"):
            all_params = get_available_parameters(df)
            st.write(f"Total parameter lever: {len(all_params)}")
            cols = st.columns(3)
            for idx, param in enumerate(all_params):
                with cols[idx % 3]:
                    st.markdown(f"• {param}")
        return
    
    # Tampilkan checkbox untuk setiap sistem
    selected_systems = []
    
    for system in available_systems:
        col_sys1, col_sys2 = st.columns([4, 1])
        with col_sys1:
            if st.checkbox(system['display'], key=f"sys_{system['key']}"):
                selected_systems.append(system['key'])
        with col_sys2:
            st.caption(f"{len(system['info']['params'])} param")
    
    if not selected_systems:
        st.warning("⚠️ Silakan pilih minimal satu sistem untuk melihat monitoring parameter.")
        return
    
    st.success(f"✅ **{len(selected_systems)} sistem dipilih**")
    
    # Tampilkan parameter untuk setiap sistem yang dipilih
    for model_key in selected_systems:
        model_info = valid_model_mapping[model_key]
        
        st.markdown(f"### {model_info['icon']} {model_info['name']}")
        st.caption(f"*{model_info['description']}*")
        
        # Tampilkan statistik sistem
        col_stat1, col_stat2 = st.columns(2)
        
        with col_stat1:
            st.metric(
                "Total Parameter", 
                f"{len(model_info['params'])}", 
                "parameter"
            )
        
        with col_stat2:
            # Hitung metrik kinerja
            param_with_data = 0
            total_delta = 0
            
            for param_base in model_info['params']:
                current_val = get_parameter_value(current_data, param_base, '_now')
                delta_val = get_parameter_value(current_data, param_base, '_delta')
                
                if current_val is not None and delta_val is not None:
                    param_with_data += 1
                    total_delta += abs(delta_val)
            
            if param_with_data > 0:
                avg_delta = total_delta / param_with_data
                st.metric(
                    "Perubahan Rata-rata", 
                    f"{avg_delta:.3f}", 
                    f"{param_with_data} parameter"
                )
            else:
                st.metric("Kinerja Sistem", "N/A", "data tidak tersedia")
        
        st.markdown("---")
        
        # Tampilkan parameter cards
        st.markdown("#### 📊 Parameter Detail")
        
        if model_info['params']:
            # Buat tabs untuk view yang berbeda
            view_tab1, view_tab2 = st.tabs(["🎯 Kartu Parameter", "📋 Tabel Parameter"])
            
            with view_tab1:
                # Tampilkan dalam bentuk kartu
                cols_per_row = 3
                for i in range(0, len(model_info['params']), cols_per_row):
                    cols = st.columns(cols_per_row)
                    for j in range(cols_per_row):
                        if i + j < len(model_info['params']):
                            param_base = model_info['params'][i + j]
                            with cols[j]:
                                # Get current, delta, and optimized values
                                current_val = get_parameter_value(current_data, param_base, '_now')
                                delta_val = get_parameter_value(current_data, param_base, '_delta')
                                opt_val = get_parameter_value(current_data, param_base, '_optimized')
                                
                                if current_val is not None:
                                    unit = get_parameter_unit(param_base)
                                    
                                    # Tentukan arah rekomendasi
                                    if delta_val is not None:
                                        if delta_val > 0:
                                            direction = "↑ Naik"
                                            direction_color = "#D50032"
                                        elif delta_val < 0:
                                            direction = "↓ Turun"
                                            direction_color = "#10B981"
                                        else:
                                            direction = "→ Stabil"
                                            direction_color = "#64748B"
                                        
                                        # Hitung persentase perubahan
                                        if current_val != 0:
                                            pct_change = (delta_val / abs(current_val)) * 100
                                        else:
                                            pct_change = 0
                                        
                                        st.markdown(f"""
                                        <div class="pln-param-card">
                                            <div style="font-size: 0.85rem; color: #64748B; font-weight: 600; margin-bottom: 0.75rem; 
                                                        display: flex; justify-content: space-between; align-items: center;">
                                                <span>{param_base}</span>
                                                <span style="font-size: 0.75rem; color: {direction_color}; 
                                                          font-weight: 700;">
                                                    {direction}
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
                                                    <div style="font-size: 1rem; font-weight: 700;" class="{'value-positive' if delta_val < 0 else 'value-negative'}">
                                                        {'+' if delta_val > 0 else ''}{delta_val:,.2f}{unit}
                                                    </div>
                                                    <div style="font-size: 0.75rem; color: #64748B; margin-top: 0.25rem;">
                                                        {pct_change:+.1f}%
                                                    </div>
                                                </div>
                                                <div style="text-align: center;">
                                                    <div style="font-size: 1.1rem; font-weight: 700; color: #10B981;">
                                                        {opt_val:,.2f}{unit if opt_val is not None else ''}
                                                    </div>
                                                    <div style="font-size: 0.75rem; color: #64748B; margin-top: 0.25rem;">
                                                        Target
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        """, unsafe_allow_html=True)
                                    else:
                                        st.info(f"Data delta tidak tersedia untuk {param_base}")
                                else:
                                    st.info(f"Data tidak tersedia untuk {param_base}")
            
            with view_tab2:
                # Tampilkan dalam bentuk tabel
                table_data = []
                for param_base in model_info['params']:
                    current_val = get_parameter_value(current_data, param_base, '_now')
                    delta_val = get_parameter_value(current_data, param_base, '_delta')
                    opt_val = get_parameter_value(current_data, param_base, '_optimized')
                    
                    if current_val is not None and delta_val is not None:
                        unit = get_parameter_unit(param_base)
                        
                        # Hitung persentase perubahan
                        if current_val != 0:
                            pct_change = (delta_val / abs(current_val)) * 100
                        else:
                            pct_change = 0
                        
                        # Tentukan arah rekomendasi
                        if delta_val > 0:
                            direction = "↑ Naik"
                        elif delta_val < 0:
                            direction = "↓ Turun"
                        else:
                            direction = "→ Stabil"
                        
                        table_data.append({
                            'Parameter': param_base,
                            'Sekarang': f"{current_val:,.2f}{unit}",
                            'Target': f"{opt_val:,.2f}{unit}" if opt_val is not None else "N/A",
                            'Perubahan': f"{delta_val:+,.2f}{unit}",
                            'Perubahan %': f"{pct_change:+.1f}%",
                            'Rekomendasi': direction
                        })
                
                if table_data:
                    table_df = pd.DataFrame(table_data)
                    
                    # Styling tabel
                    def color_recommendation(val):
                        if "↑ Naik" in val:
                            color = '#D50032'
                        elif "↓ Turun" in val:
                            color = '#10B981'
                        else:
                            color = '#64748B'
                        return f'color: {color}; font-weight: 700;'
                    
                    styled_df = table_df.style.applymap(color_recommendation, subset=['Rekomendasi'])
                    
                    st.dataframe(
                        styled_df,
                        use_container_width=True,
                        height=min(400, len(table_data) * 35 + 50)
                    )
                else:
                    st.warning("Tidak ada data parameter yang tersedia untuk sistem ini.")
        
        st.markdown("---")
    
    # Footer informasi
    st.markdown("""
    <div style="background: #F8FAFC; padding: 1rem; border-radius: 10px; border-left: 4px solid #0033A0; margin-top: 2rem;">
        <div style="font-size: 0.9rem; color: #64748B;">
            <strong>📝 Panduan Interpretasi Parameter:</strong> 
            <ul style="margin-top: 0.5rem;">
                <li><span style="color: #D50032; font-weight: 700;">↑ Naik (Merah)</span>: Parameter perlu dinaikkan menuju nilai target untuk optimasi NPHR</li>
                <li><span style="color: #10B981; font-weight: 700;">↓ Turun (Hijau)</span>: Parameter perlu diturunkan menuju nilai target untuk optimasi NPHR</li>
                <li><span style="color: #64748B; font-weight: 700;">→ Stabil (Abu)</span>: Parameter sudah mendekati nilai target</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)