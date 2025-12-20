import plotly.graph_objects as go

def create_gauge_chart(current_value, baseline_value, title):
    """Buat gauge chart dengan tema PLN"""
    
    # Hitung rentang yang lebih reasonable
    min_val = min(current_value, baseline_value) * 0.95
    max_val = max(current_value, baseline_value) * 1.05
    
    # Pastikan ada cukup space untuk melihat delta
    range_padding = abs(current_value - baseline_value) * 2
    min_val = min(min_val, min(current_value, baseline_value) - range_padding)
    max_val = max(max_val, max(current_value, baseline_value) + range_padding)
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=float(current_value),
        title={
            'text': title,
            'font': {'size': 16, 'color': '#0033A0'}
        },
        delta={
            'reference': float(baseline_value),
            'relative': False,
            'increasing': {'color': "#10B981"},
            'decreasing': {'color': "#D50032"},
            'font': {'size': 14},
            'suffix': ' kcal/kWh'
        },
        gauge={
            'axis': {
                'range': [min_val, max_val],
                'tickwidth': 1,
                'tickcolor': "#0033A0",
                'tickformat': ',.0f',
                'dtick': (max_val - min_val) / 5,
                'tickmode': 'linear'
            },
            'bar': {'color': "#0033A0"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "#E5E7EB",
            'steps': [
                {'range': [min_val, baseline_value], 'color': "#F1F5F9"},
                {'range': [baseline_value, current_value], 'color': "#93C5FD"} if current_value > baseline_value
                else {'range': [current_value, baseline_value], 'color': "#FEE2E2"}
            ],
            'threshold': {
                'line': {'color': "#D50032", 'width': 3},
                'thickness': 0.85,
                'value': float(baseline_value)
            }
        },
        number={
            'font': {'size': 28, 'color': '#0033A0'},
            'valueformat': ',.0f',
            'suffix': ' kcal/kWh'
        },
        domain={'row': 0, 'column': 0}
    ))
    
    fig.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=60, b=80),
        paper_bgcolor="rgba(0,0,0,0)",
        font={'family': "Arial, sans-serif"}
    )
    return fig