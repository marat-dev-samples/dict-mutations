DATA_SAMPLE = {
    "id":"1527617024",            # Put real schema id for this test
    "name": "Test",
    #"date":"18-02-2020",
    #"time":"14:45",
    "enable":"off",
    "currency":"GBPUSD",
    "dev": {
        'ma_val': {
            'id': 'ma_val',
            'display_name': 'Moving averange', 
            'type_id': '550', 
            'top': 0, 
            'left': 550,
            'params': {
                
                'l_in': {'position': 'LeftMiddle', 'id': 'l_in', 'value': ''},
                'l_out': {'position': 'RightMiddle', 'info_arr': 'line', 'display_name': 'line', 'id': 'l_out', 'value': 'off'},
                'l_info': {'id': 'l_info', 'value': '', 'display_name': 'Line info', 'change': 'line_name'},
        

                's_in': {'id': 's_in', 'display_name': 'MA value', 'position': 'TopCenter', 'info_arr': 'sensor', 'value': 1.0},
                's_out': {'id': 's_out', 'display_name': 'MA value', 'position': 'TopCenter', 'info_arr': 'sensor', 'value': 0.0},
                'currency': {'id': 'currency', 'display_name': 'Currency', 'change': 'currency_select', 'value': 'GBPUSD'},
                'ma': {'id': 'ma', 'display_name': 'Smooth', 'change': 'select', 'value': 55},
                'period': {'id': 'period', 'display_name': 'Period set', 'value': 15, 'change': 'period_select'}, 
        

    
           }
        }
    }    
}


ELEMENT_SAMPLE = {
    'id': 'ma_val',
    'display_name': 'Moving averange', 
    'type_id': '550', 
    'top': 0, 
    'left': 550,
    'params': {
        'l_in': {'position': 'LeftMiddle', 'id': 'l_in', 'value': ''},
        'l_out': {'position': 'RightMiddle', 'info_arr': 'line', 'display_name': 'line', 'id': 'l_out', 'value': 'off'},
        'l_info': {'id': 'l_info', 'value': '', 'display_name': 'Line info', 'change': 'line_name'},
        'period': {'id': 'period', 'display_name': 'Period set', 'value': 15, 'change': 'period_select'}, 
    }
}


