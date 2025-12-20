import os

# ==========================
# PATH CONFIGURATION
# ==========================
# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Data paths
DATA_DIR = os.path.join(BASE_DIR, "data")
CSV_DETAILED = os.path.join(DATA_DIR, "march_2025_savings_detailed.csv")
CSV_SUMMARY = os.path.join(DATA_DIR, "march_2025_savings_summary.csv")

# ==========================
# COLOR THEME
# ==========================
COLORS = {
    'pln_blue': '#0033A0',
    'pln_red': '#D50032',
    'pln_light_blue': '#0066CC',
    'pln_gray': '#F5F7FA',
    'pln_dark_gray': '#64748B',
    'pln_green': '#10B981',
    'pln_yellow': '#F59E0B',
    'pln_orange': '#F97316',
    'pln_purple': '#8B5CF6',
}

# ==========================
# SESSION STATE DEFAULTS
# ==========================
SESSION_DEFAULTS = {
    'simulation_running': True,
    'current_index': 0,
    'window_size': 20,
    'refresh_interval': 3,
    'selected_models': []
}

# ==========================
# APP CONSTANTS
# ==========================
APP_NAME = "PLN NPHR Optimization Dashboard"
APP_ICON = "⚡"
DATA_INTERVAL = 15  # menit