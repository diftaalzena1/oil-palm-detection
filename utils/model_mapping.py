def create_model_mapping():
    """Buat mapping parameter ke sistem/komponen - SESUAIKAN DENGAN DATASET ANDA"""
    return {
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
        },
        'COND': {
            'icon': '🌡️',
            'name': 'CONDENSER SYSTEM',
            'params': [
                'HOTWELL LEVEL',
                'INLET TEMP CONDENSER',
                'OUTLET PRESS SIDE CONDENSER',
                'OUTLET TEMP CONDENSER',
                'CDST VAM',
                'RH OUT STEAM TEMP'
            ],
            'color': '#F59E0B',
            'description': 'Sistem kondenser'
        }
    }