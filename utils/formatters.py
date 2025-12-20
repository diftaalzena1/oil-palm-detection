def format_number(value, decimals=2):
    """Format angka dengan desimal dan pemisah ribuan"""
    try:
        return f"{float(value):,.{decimals}f}"
    except:
        return str(value)

def format_percentage(value):
    """Format persentase dengan 2 desimal"""
    try:
        return f"{float(value):+.2f}%"
    except:
        return str(value)

def format_currency(value):
    """Format mata uang Indonesia"""
    try:
        value = float(value)
        if value >= 1e12:
            return f"Rp {value/1e12:,.2f} T"
        elif value >= 1e9:
            return f"Rp {value/1e9:,.2f} M"
        elif value >= 1e6:
            return f"Rp {value/1e6:,.2f} juta"
        else:
            return f"Rp {value:,.0f}"
    except:
        return str(value)

def extract_parameter_base_name(column_name):
    """Ekstrak nama dasar parameter dari nama kolom"""
    suffixes = ['_now', '_delta', '_optimized', '_exo_now', '_lever_now', '_lever_delta', '_lever_optimized']
    for suffix in suffixes:
        if column_name.endswith(suffix):
            return column_name.replace(suffix, '')
    return column_name

def get_parameter_unit(param_name):
    """Dapatkan unit untuk parameter tertentu"""
    param_lower = param_name.lower()
    
    if 'temp' in param_lower or 'temperature' in param_lower:
        return '°C'
    elif 'pressure' in param_lower or 'pt' in param_lower or 'press' in param_lower:
        return ' bar' if 'main' in param_lower else ''
    elif 'flow' in param_lower:
        return ' t/h'
    elif 'level' in param_lower or 'lt' in param_lower or 'lvl' in param_lower:
        return ' mm'
    elif 'ratio' in param_lower:
        return ''
    elif 'o2' in param_lower:
        return ' %'
    elif 'air' in param_lower:
        return ' %'
    elif 'position' in param_lower or 'posi' in param_lower:
        return ' %'
    elif 'angle' in param_lower:
        return ' °'
    elif 'energy' in param_lower or 'kwh' in param_lower:
        return ' kWh'
    elif 'kcal' in param_lower:
        return ' kcal'
    elif 'kg' in param_lower:
        return ' kg'
    else:
        return ''