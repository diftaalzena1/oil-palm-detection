# modules/ui_components.py
import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import io

def image_grid_with_selection(uploaded_files, MAX_BATCH_WARNING):
    if not uploaded_files:
        return []
    
    st.subheader("Select Images to Process")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Images", len(uploaded_files))
    with col2:
        total_size = sum(f.size for f in uploaded_files) / (1024*1024)
        st.metric("Total Size", f"{total_size:.2f} MB")
    
    if len(uploaded_files) > MAX_BATCH_WARNING:
        st.warning(f"⚠️ Processing more than {MAX_BATCH_WARNING} images may be slow.")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("✓ Select All", use_container_width=True, key="select_all_btn", type="primary"):
            for key in st.session_state.keys():
                if key.startswith("img_sel_"):
                    st.session_state[key] = True
            st.rerun()
    with col_btn2:
        if st.button("✗ Clear All", use_container_width=True, key="clear_all_btn"):
            for key in st.session_state.keys():
                if key.startswith("img_sel_"):
                    st.session_state[key] = False
            st.rerun()
    
    st.markdown("---")
    
    selected = []
    cols_per_row = 3
    num_files = len(uploaded_files)
    for i in range(0, num_files, cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            idx = i + j
            if idx < num_files:
                file = uploaded_files[idx]
                img = Image.open(file).convert("RGB")
                img.thumbnail((180, 180))
                with col:
                    st.image(img, use_container_width=True)
                    checked = st.checkbox(
                        file.name,
                        value=st.session_state.get(f"img_sel_{idx}", False),
                        key=f"img_sel_{idx}"
                    )
                    if checked:
                        selected.append(idx)
    
    if selected:
        st.success(f"✓ {len(selected)} image(s) selected")
    else:
        st.info("ℹ️ Please select at least one image")
    
    return selected

def plot_interactive_map(coords, img_shape, max_size=700):
    """
    Menampilkan tree map dengan proporsi yang sama persis dengan gambar asli.
    
    Parameters:
    - coords: list of (x, y) koordinat pohon
    - img_shape: (height, width) gambar asli
    - max_size: ukuran maksimal sisi terpanjang (pixel)
    """
    if not coords:
        return None
    
    h, w = img_shape
    df = pd.DataFrame(coords, columns=['x', 'y'])
    
    # Hitung ukuran plot berdasarkan rasio gambar
    if w >= h:
        plot_width = max_size
        plot_height = int(max_size * h / w)
    else:
        plot_height = max_size
        plot_width = int(max_size * w / h)
    
    fig = px.scatter(
        df, x='x', y='y', 
        title=f"Tree Map ({len(coords)} trees) - Rasio {w}x{h}",
        labels={'x': 'X (px)', 'y': 'Y (px)'}, 
        width=plot_width,
        height=plot_height
    )
    
    fig.update_yaxes(autorange="reversed")
    
    # Pastikan rasio aspek 1:1 (1 pixel = 1 unit)
    fig.update_layout(
        plot_bgcolor='white', 
        paper_bgcolor='white',
        font=dict(color='#1e293b'),
        xaxis=dict(
            scaleanchor="y",  # Sumbu X mengikuti sumbu Y
            scaleratio=1,     # 1 unit X = 1 unit Y
            constrain="domain"
        ),
        yaxis=dict(
            scaleanchor="x",
            scaleratio=1
        )
    )
    
    fig.update_traces(
        marker=dict(size=8, color='#2c6e49', line=dict(width=1, color='white'))
    )
    
    return fig

def display_metric_card(label, value, bg_color, text_color="white"):
    st.markdown(f"""
        <div style="background-color: {bg_color}; padding: 0.8rem; border-radius: 10px; text-align: center; margin: 0.2rem;">
            <p style="margin:0; font-size:0.9rem; color:{text_color};">{label}</p>
            <p style="margin:0; font-size:1.6rem; font-weight:bold; color:{text_color};">{value}</p>
        </div>
    """, unsafe_allow_html=True)

def get_demo_images():
    import os
    from config import DEMO_FOLDER
    if not os.path.exists(DEMO_FOLDER):
        return []
    files = [f for f in os.listdir(DEMO_FOLDER) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    return sorted(files)

def load_demo_image_from_file(filename):
    import os
    from PIL import Image
    from config import DEMO_FOLDER
    path = os.path.join(DEMO_FOLDER, filename)
    if os.path.exists(path):
        return Image.open(path).convert("RGB")
    return None
