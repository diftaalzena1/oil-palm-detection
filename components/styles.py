import streamlit as st

def load_css():
    """Load custom CSS untuk tema PLN"""
    st.markdown("""
    <style>
        /* Warna tema PLN - Biru dan Merah */
        :root {
            --pln-blue: #0033A0;
            --pln-red: #D50032;
            --pln-light-blue: #0066CC;
            --pln-gray: #F5F7FA;
            --pln-dark-gray: #64748B;
            --pln-green: #10B981;
            --pln-yellow: #F59E0B;
            --pln-orange: #F97316;
            --pln-purple: #8B5CF6;
        }
        
        .main-header {
            font-size: 2.8rem;
            color: var(--pln-blue);
            font-weight: 800;
            margin-bottom: 0.5rem;
            background: linear-gradient(135deg, var(--pln-blue) 0%, var(--pln-light-blue) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .sub-header {
            font-size: 1.3rem;
            color: var(--pln-dark-gray);
            margin-bottom: 2rem;
            font-weight: 500;
        }
        
        .pln-metric-card {
            background: linear-gradient(135deg, #ffffff 0%, var(--pln-gray) 100%);
            padding: 1.5rem;
            border-radius: 15px;
            color: var(--pln-blue);
            box-shadow: 0 6px 15px rgba(0, 51, 160, 0.1);
            border-left: 5px solid var(--pln-red);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            height: 100%;
        }
        
        .pln-metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0, 51, 160, 0.15);
        }
        
        .pln-metric-value {
            font-size: 2.2rem;
            font-weight: 800;
            color: var(--pln-blue);
            margin-top: 0.5rem;
        }
        
        .pln-metric-label {
            font-size: 0.95rem;
            color: var(--pln-dark-gray);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .pln-improvement-positive {
            color: var(--pln-green) !important;
            font-weight: 700;
        }
        
        .pln-improvement-negative {
            color: var(--pln-red) !important;
            font-weight: 700;
        }
        
        .pln-badge {
            background: linear-gradient(135deg, var(--pln-red) 0%, #FF6B6B 100%);
            color: white;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            display: inline-block;
            margin-left: 0.5rem;
        }
        
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, var(--pln-blue) 0%, var(--pln-light-blue) 100%);
        }
        
        .stButton > button {
            background: linear-gradient(135deg, var(--pln-blue) 0%, var(--pln-light-blue) 100%);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 10px;
            font-weight: 700;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(0, 51, 160, 0.2);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0, 51, 160, 0.25);
            background: linear-gradient(135deg, var(--pln-light-blue) 0%, var(--pln-blue) 100%);
        }
        
        .pln-section-header {
            font-size: 1.5rem;
            color: var(--pln-blue);
            font-weight: 700;
            margin-bottom: 1.5rem;
            padding-bottom: 0.5rem;
            border-bottom: 3px solid var(--pln-red);
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }
        
        .pln-info-box {
            background: linear-gradient(135deg, #E3F2FD 0%, #F3E5F5 100%);
            padding: 1.25rem;
            border-radius: 12px;
            border-left: 4px solid var(--pln-blue);
            margin: 1rem 0;
        }
        
        .pln-param-card {
            background: white;
            padding: 1rem;
            border-radius: 10px;
            border: 1px solid #E5E7EB;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
        }
        
        .pln-param-card:hover {
            border-color: var(--pln-blue);
            box-shadow: 0 4px 8px rgba(0, 51, 160, 0.1);
        }
        
        .stTabs [data-baseweb="tab-list"] {
            gap: 2px;
            background-color: var(--pln-gray);
            padding: 5px;
            border-radius: 10px;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: white;
            border-radius: 8px 8px 0 0;
            padding: 10px 20px;
            font-weight: 600;
            color: var(--pln-dark-gray);
        }
        
        .stTabs [aria-selected="true"] {
            background-color: var(--pln-blue) !important;
            color: white !important;
        }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.6; }
            100% { opacity: 1; }
        }
        
        .real-time-badge {
            animation: pulse 2s infinite;
            background: linear-gradient(135deg, #10B981, #34D399);
            color: white;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            display: inline-block;
            margin-left: 0.5rem;
        }
        
        @keyframes valueChange {
            0% { background-color: transparent; }
            50% { background-color: rgba(16, 185, 129, 0.2); }
            100% { background-color: transparent; }
        }
        
        .value-changing {
            animation: valueChange 1s ease;
        }
        
        .status-indicator {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 8px;
        }
        
        .status-active {
            background-color: var(--pln-green);
            box-shadow: 0 0 10px var(--pln-green);
        }
        
        .status-warning {
            background-color: var(--pln-yellow);
            box-shadow: 0 0 10px var(--pln-yellow);
        }
        
        .value-positive {
            color: #10B981 !important;
            font-weight: 700;
        }
        
        .value-negative {
            color: #D50032 !important;
            font-weight: 700;
        }
        
        .cost-saving-card {
            background: linear-gradient(135deg, #10B981 0%, #34D399 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 15px;
            box-shadow: 0 6px 15px rgba(16, 185, 129, 0.2);
            height: 100%;
        }
        
        .coal-saving-card {
            background: linear-gradient(135deg, #F59E0B 0%, #FBBF24 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 15px;
            box-shadow: 0 6px 15px rgba(245, 158, 11, 0.2);
            height: 100%;
        }
        
        .efficiency-card {
            background: linear-gradient(135deg, #3B82F6 0%, #60A5FA 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 15px;
            box-shadow: 0 6px 15px rgba(59, 130, 246, 0.2);
            height: 100%;
        }
        
        .improvement-card {
            background: linear-gradient(135deg, #8B5CF6 0%, #A78BFA 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 15px;
            box-shadow: 0 6px 15px rgba(139, 92, 246, 0.2);
            height: 100%;
        }
    </style>
    """, unsafe_allow_html=True)