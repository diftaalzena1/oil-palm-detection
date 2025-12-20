import streamlit as st
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import SESSION_DEFAULTS
from components.styles import load_css
from components.sidebar import render_sidebar
from components.header import render_header
from components.kpi_cards import render_kpi_section
from tabs.main_dashboard import render_main_dashboard
from tabs.system_monitoring import render_system_monitoring
from tabs.exogenous_params import render_exogenous_params
from tabs.impact_analysis import render_impact_analysis
from utils.data_loader import load_detailed_data, load_summary_data

# ==========================
# PAGE CONFIGURATION
# ==========================
st.set_page_config(
    page_title="PLN NPHR Optimization Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================
# LOAD CUSTOM CSS
# ==========================
load_css()

# ==========================
# INITIALIZE SESSION STATE
# ==========================
for key, value in SESSION_DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ==========================
# LOAD DATA
# ==========================
@st.cache_resource
def initialize_data():
    df = load_detailed_data()
    summary_df = load_summary_data()
    return df, summary_df

df, summary_df = initialize_data()

if df.empty:
    st.warning("⚠️ Data tidak tersedia. Mohon pastikan file CSV ada di folder 'data/'")
    st.stop()

# ==========================
# RENDER COMPONENTS
# ==========================
render_header()
render_sidebar(df)
render_kpi_section(df)

# ==========================
# MAIN CONTENT - TABS
# ==========================
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 DASHBOARD UTAMA", 
    "🔧 MONITORING SISTEM", 
    "🌡️ PARAMETER EXOGENOUS",
    "💰 IMPACT ANALYSIS"
])

with tab1:
    render_main_dashboard(df)

with tab2:
    render_system_monitoring(df)

with tab3:
    render_exogenous_params(df)

with tab4:
    render_impact_analysis(df, summary_df)

# ==========================
# SIMULATION CONTROL
# ==========================
from components.simulation_control import render_simulation_control
render_simulation_control(df)