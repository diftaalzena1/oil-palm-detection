# config.py
import streamlit as st
import os

# PAGE CONFIG
st.set_page_config(
    page_title="Oil Palm Detection System",
    layout="wide",
    page_icon="🌴",
    initial_sidebar_state="expanded"
)

# CONSTANTS
MODEL_PATH = "models/model_clahe_v3.pt"
BOX_RAW = (170, 170, 170)
CENTROID_CLUSTER = (255, 0, 0)
FINAL_TREE = (0, 255, 0)
MAX_BATCH_WARNING = 20
DEMO_FOLDER = "demo"