# app.py
import streamlit as st
import time
import gc
import numpy as np
from PIL import Image
import pandas as pd
import io
from datetime import datetime

# Import konfigurasi
import config
from config import get_recommendation

# Custom CSS
st.markdown("""
    <style>
    .block-container {
        max-width: 1400px !important;
        margin: 0 auto !important;
    }
    </style>
""", unsafe_allow_html=True)

# Import modul
from modules.sahi_detector import get_model, process_image
from modules.exporter import export_to_zip, export_to_excel
from modules.ui_components import (
    image_grid_with_selection, plot_interactive_map, get_demo_images, load_demo_image_from_file
)

# SESSION STATE INIT
if "batch_results" not in st.session_state:
    st.session_state.batch_results = []
if "processing_cancel" not in st.session_state:
    st.session_state.processing_cancel = False
if "settings" not in st.session_state:
    st.session_state.settings = {
        "use_sahi": True,
        "conf_thres": 0.25,
        "use_clahe": True,
        "use_dbscan": True,
        "eps_factor": 0.6,
        "luas_ha": 10.0,
        "land_type": "Mineral"
    }
if "demo_loaded" not in st.session_state:
    st.session_state.demo_loaded = False

# MAIN APP
st.title("🌴 Oil Palm Detection System")
st.caption("AI-Driven Analytics for Sustainable Plantation Management")

# Sidebar settings
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    tab1, tab2, tab3 = st.tabs(["Plantation", "Detection", "Help"])
    
    with tab1:
        st.session_state.settings["luas_ha"] = st.number_input(
            "Area (Hectares)", 0.1, 100.0,
            st.session_state.settings["luas_ha"], 0.5,
            help="Total plantation area in hectares"
        )
        st.session_state.settings["land_type"] = st.selectbox(
            "Land Type",
            ["Mineral", "Peat (Gambut)", "Hilly (Bukit)"],
            index=["Mineral","Peat (Gambut)","Hilly (Bukit)"].index(st.session_state.settings["land_type"]),
            help="Type of plantation land"
        )
    
    with tab2:
        st.session_state.settings["use_sahi"] = st.checkbox(
            "Use SAHI Sliced Inference", st.session_state.settings["use_sahi"],
            help="Sliced inference for large images"
        )
        st.session_state.settings["conf_thres"] = st.slider(
            "Confidence Threshold", 0.1, 0.9,
            st.session_state.settings["conf_thres"], 0.05
        )
        st.session_state.settings["use_clahe"] = st.checkbox(
            "LAB + CLAHE Enhancement", st.session_state.settings["use_clahe"]
        )
        st.session_state.settings["use_dbscan"] = st.checkbox(
            "Smart Counting (DBSCAN)", st.session_state.settings["use_dbscan"]
        )
        st.session_state.settings["eps_factor"] = st.slider(
            "Clustering Sensitivity", 0.3, 1.0,
            st.session_state.settings["eps_factor"], 0.05
        )
    
    with tab3:
        st.markdown("""
        **Panduan & Tips**
        - **SAHI**: Gunakan untuk gambar besar (>2K px) agar tidak error memori.
        - **DBSCAN**: Menghilangkan deteksi ganda dari potongan gambar yang tumpang tindih.
        - **CLAHE**: Meningkatkan kontras gambar gelap atau berkabut.
        - **Status Kepadatan**: Berdasarkan jenis lahan & luas area yang diinput.
        - **Ekspor**: ZIP (gambar+CSV), Excel (ringkasan+koordinat).

        ---

        **Standar Kepadatan Ideal (pohon per hektar):**

        | Jenis Lahan | Kepadatan Ideal | Keterangan |
        |-------------|-----------------|-------------|
        | Mineral | 136 - 148 | Lahan subur, kepadatan standar |
        | Peat (Gambut) | 110 - 130 | Lahan gambut, kepadatan lebih rendah |
        | Hilly (Bukit) | 100 - 120 | Lahan berbukit, akses terbatas |

        > Catatan: Kepadatan = Total Pohon ÷ Luas Area (hektar)

        **Status yang Muncul:**
        - 🟢 **OPTIMAL** : Kepadatan dalam range ideal
        - 🔴 **UNDERPOPULATED** : Di bawah range ideal (kurang produktif → perlu tanam ulang)
        - 🟠 **OVERPOPULATED** : Di atas range ideal (terlalu padat → perlu panen/penjarangan)
        ---
        """)
        
        demo_files = get_demo_images()
        if demo_files:
            st.markdown("**Coba dengan gambar demo**")
            selected_demo = st.selectbox("Pilih gambar contoh:", demo_files, key="demo_select")
            if st.button("Muat Gambar Demo", use_container_width=True):
                with st.spinner(f"Memuat {selected_demo}..."):
                    img = load_demo_image_from_file(selected_demo)
                    if img:
                        img_bytes = io.BytesIO()
                        img.save(img_bytes, format='JPEG')
                        img_data = img_bytes.getvalue()
                        class DemoFile:
                            def __init__(self, name, data):
                                self.name = name
                                self._data = data
                            def read(self):
                                return self._data
                            def getvalue(self):
                                return self._data
                            @property
                            def size(self):
                                return len(self._data)
                        st.session_state.demo_image = DemoFile(selected_demo, img_data)
                        st.session_state.demo_loaded = True
                        st.rerun()
        else:
            st.info("📁 Tidak ada gambar demo. Silakan tambahkan gambar ke folder 'demo'.")
    
    if st.button("Reset to Defaults", use_container_width=True):
        st.session_state.settings = {
            "use_sahi": True, "conf_thres": 0.25, "use_clahe": True, "use_dbscan": True,
            "eps_factor": 0.6, "luas_ha": 10.0, "land_type": "Mineral"
        }
        st.rerun()

# Load model
model = get_model(st.session_state.settings["use_sahi"], st.session_state.settings["conf_thres"])

# Main area: upload
st.header("1. Upload Images")
uploaded_files = st.file_uploader(
    "Drag & drop or browse aerial images (JPG, PNG)",
    type=["jpg","jpeg","png"],
    accept_multiple_files=True,
    help="Supports up to 100MB per file. For large images, enable SAHI."
)

# Demo image handling
if st.session_state.get("demo_loaded", False) and 'demo_image' in st.session_state:
    demo_file = st.session_state.demo_image
    if uploaded_files is None:
        uploaded_files = [demo_file]
    else:
        if not any(f.name == demo_file.name for f in uploaded_files):
            uploaded_files = [demo_file] + list(uploaded_files)
    st.success(f"✅ Demo image '{demo_file.name}' loaded! You can select it below.")

if uploaded_files:
    selected_indices = image_grid_with_selection(uploaded_files, config.MAX_BATCH_WARNING)
    
    if selected_indices and st.button("▶ Start Detection", type="primary", use_container_width=True):
        st.session_state.processing_cancel = False
        params = {
            'use_sahi': st.session_state.settings["use_sahi"],
            'conf_thres': st.session_state.settings["conf_thres"],
            'use_clahe': st.session_state.settings["use_clahe"],
            'use_dbscan': st.session_state.settings["use_dbscan"],
            'eps_factor': st.session_state.settings["eps_factor"],
            'model': model
        }
        
        results = []
        status_container = st.status("Processing images...", expanded=True)
        progress_bar = st.progress(0)
        cancel_btn = st.button("❌ Cancel", key="cancel_process")
        
        start_time = time.time()
        for i, idx in enumerate(selected_indices):
            if cancel_btn or st.session_state.processing_cancel:
                st.session_state.processing_cancel = True
                status_container.update(label="❌ Cancelled by user", state="error")
                break
            file = uploaded_files[idx]
            status_container.write(f"Processing **{file.name}** ({i+1}/{len(selected_indices)})")
            elapsed = time.time() - start_time
            if i > 0:
                est_remaining = (elapsed / i) * (len(selected_indices) - i)
                status_container.write(f"⏱️ Estimated remaining: {est_remaining:.1f} seconds")
            
            img = np.array(Image.open(file).convert("RGB"))
            res = process_image(img, params)
            res['filename'] = file.name
            density = res['total_trees'] / st.session_state.settings["luas_ha"] if st.session_state.settings["luas_ha"] > 0 else 0
            res['density'] = density
            land = st.session_state.settings["land_type"]
            ideal = {"Mineral": (136,148), "Peat (Gambut)": (110,130), "Hilly (Bukit)": (100,120)}[land]
            if density < ideal[0]:
                res['status'] = "UNDERPOPULATED"
            elif density > ideal[1]:
                res['status'] = "OVERPOPULATED"
            else:
                res['status'] = "OPTIMAL"
            results.append(res)
            progress_bar.progress((i+1)/len(selected_indices))
            gc.collect()
        
        if not st.session_state.processing_cancel:
            status_container.update(label="✅ Detection completed!", state="complete")
            st.session_state.batch_results = results
            st.toast(f"{len(results)} images processed successfully!", icon="✅")
            st.rerun()
        else:
            status_container.update(label="Processing cancelled", state="error")
    
    # Show batch results
    if st.session_state.batch_results:
        st.header("2. Batch Results")
        
        df_res = pd.DataFrame([{
            'Image': r['filename'],
            'Trees': r['total_trees'],
            'Density (trees/ha)': f"{r['density']:.1f}",
            'Status': r['status'],
            'Recommendation': get_recommendation(r['status'])  # tambah ini
        } for r in st.session_state.batch_results])
        
        def highlight_status(val):
            if val == 'OPTIMAL':
                return 'background-color: #ccffcc'
            elif val == 'UNDERPOPULATED':
                return 'background-color: #ffcccc'
            else:
                return 'background-color: #ffe6cc'
        
        styled_df = (df_res.style
            .map(highlight_status, subset=['Status'])
            .set_properties(**{'text-align': 'center'})
            .set_table_styles([
                {'selector': 'th', 'props': [
                    ('background-color', '#ffffff'),
                    ('color', '#333333'),
                    ('text-align', 'center'),
                    ('font-weight', '600'),
                    ('border-bottom', '2px solid #dddddd')
                ]}
            ])
        )
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
        
        st.subheader("Image Details")
        for idx, res in enumerate(st.session_state.batch_results):
            with st.expander(f"{res['filename']} — {res['total_trees']} trees ({res['status']})"):
                col_img, col_metrics = st.columns([2, 1])
                with col_img:
                    st.image(res['annotated'], use_container_width=True, caption="Annotated Result")
                with col_metrics:
                    row1_col1, row1_col2 = st.columns(2)
                    with row1_col1:
                        st.metric("Final Trees", res['total_trees'])
                    with row1_col2:
                        st.metric("Density", f"{res['density']:.1f}")
                    row2_col1, row2_col2 = st.columns(2)
                    with row2_col1:
                        st.metric("Raw Detections", res['raw_detections'])
                    with row2_col2:
                        st.metric("Avg Confidence", f"{res['avg_conf']:.3f}")
                    
                    status = res['status']
                    if status == "OPTIMAL":
                        chip_color = "#2e7d32"
                        bg_color = "#e8f5e9"
                        rec_text = "Lanjutkan pengelolaan normal"
                    elif status == "UNDERPOPULATED":
                        chip_color = "#c62828"
                        bg_color = "#ffebee"
                        rec_text = "Perlu penanaman ulang (replanting) di area kosong"
                    else:
                        chip_color = "#ed6c02"
                        bg_color = "#fff4e5"
                        rec_text = "Perlu pemanenan atau penjarangan (thinning)"
                    
                    # Status chip
                    st.markdown(f"""
                        <div style="margin-top: 0.5rem; padding: 0.4rem 0.8rem; background-color: {bg_color}; border-radius: 20px; text-align: center;">
                            <span style="color: {chip_color}; font-weight: 500; font-size: 0.8rem;">Status</span><br>
                            <span style="color: #1e293b; font-weight: 600; font-size: 0.9rem;">{status}</span>
                        </div>
                    """, unsafe_allow_html=True)

                    # Rekomendasi dengan warna yang sama
                    st.markdown(f"""
                        <div style="margin-top: 0.5rem; padding: 0.4rem 0.8rem; background-color: {bg_color}; border-radius: 20px; text-align: center;">
                            <span style="color: {chip_color}; font-weight: 500; font-size: 0.8rem;">Rekomendasi</span><br>
                            <span style="color: #1e293b; font-weight: 500; font-size: 0.85rem;">{rec_text}</span>
                        </div>
                    """, unsafe_allow_html=True)
                
                if res['coords']:
                    show_map = st.checkbox(f"🗺️ Show Tree Map", key=f"show_map_{idx}")
                    if show_map:
                        st.plotly_chart(plot_interactive_map(res['coords'], res['img_shape']), use_container_width=True)
                
                if res['slice_previews']:
                    total_slices = len(res['slice_previews'])
                    total_dets = sum(res['slice_counts'])
                    show_slices = st.checkbox(f"🔍 Show SAHI Slices Preview ({total_slices} slices, {total_dets} detections)", key=f"show_slices_{idx}")
                    if show_slices:
                        slice_cols = st.columns(3)
                        for j, slice_img in enumerate(res['slice_previews'][:12]):
                            with slice_cols[j % 3]:
                                st.image(slice_img, caption=f"Slice {j+1} | {res['slice_counts'][j]} det.", use_container_width=True)
                        if total_slices > 12:
                            st.caption(f"... and {total_slices - 12} more slices not shown.")
                
                col_dl1, col_dl2 = st.columns(2)
                img_bytes = io.BytesIO()
                Image.fromarray(res['annotated']).save(img_bytes, format='PNG')
                col_dl1.download_button("Download Image", img_bytes.getvalue(), f"{res['filename']}_annotated.png", key=f"dl_img_{idx}", use_container_width=True)
                if res['coords']:
                    df_coords = pd.DataFrame(res['coords'], columns=['x','y'])
                    col_dl2.download_button("Download CSV", df_coords.to_csv(index=False), f"{res['filename']}_coords.csv", key=f"dl_csv_{idx}", use_container_width=True)
        
        # Export section
        st.subheader("Export All Results")
        col_zip, col_excel = st.columns(2)
        with col_zip:
            zip_data = export_to_zip(st.session_state.batch_results)
            st.download_button("ZIP (images+CSV)", zip_data,
                               f"batch_{datetime.now():%Y%m%d_%H%M%S}.zip",
                               mime="application/zip", use_container_width=True)
        with col_excel:
            excel_data = export_to_excel(st.session_state.batch_results)
            st.download_button("Excel Report", excel_data,
                               f"report_{datetime.now():%Y%m%d_%H%M%S}.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                               use_container_width=True)
        
        if st.button("🗑️ Clear All Results", use_container_width=True):
            st.session_state.batch_results = []
            st.session_state.demo_loaded = False
            st.rerun()
else:
    st.info("📤 Upload plantation aerial images or click 'Load Demo Image' in the Help tab to begin analysis.")

# Footer
st.markdown("""
    <hr>
    <div style='text-align: center; color: gray;'>
    Oil Palm Detection System
    </div>
""", unsafe_allow_html=True)
