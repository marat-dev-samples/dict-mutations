import random
from typing import Dict


"""
ToDo:
    
    Server execution security param
    Created/Tested

    ++ MA select                  1-255 -> rename to Smooth
    ++ Period select              5, 15, 60, 240
    +- Available currency         ['GBPUSD', 'EURUSD']
    -- On/off                     ['on', 'off']  
    -- type_id (module name)      1-100000000 
    -- position                   ['TopCenter', 'BottomLeft'] 
    -- change ?                    ['switch', 'display', 'order', 'text', 'color_select', 
                                   'currency_select', 'period_select', 'bars_slider', 
                                   'param_slider','alarm_select', 'line_name', 'null', 
                                   'range_slider', 'sensor_order', 'timer'
                                   ]
    
    -- Short name (Param name) String lengh 30 symbols, replace all excluding A-Z, a-z, 0-9, '+-=<>@$:;,.!?' 
    -- Long name (Flowchart name) String lengh 30 symbols, replace all excluding A-Z, a-z, 0-9, '+-=<>@$:;,.!?' 

    
   
    top, left -> int positive

    Hazardus params:
    + type_id        -> not valid module name
    + schema_id      -> for change
    - ma             -> not in range
    - prohibited symbols
    - nested json


    Query:
        - data query and update

    Mutation:
        - update data    - returns data
        - create element - returns element data (json string)
        - delete element - status = success
        - return schema data (json string)

    Todo:
       - Long string
       + Put Data directly - context
       - Create github brunch - nesting_update
       - Comments, flake8 


"""


#AVAILABLE_QUOTES = ['GBPUSD', 'EURUSD']


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






def new_element(type_id: int) -> Dict[str, Dict] :
    """Retrieve element's data by it's type_id and, also generates unique id for new element"""
    
    print(f'Element type: {type_id}')
    el_data = ELEMENT_SKELETON  
    el_id = f"{el_data.get('id')}{random.randint(100, 900)}"
    return {el_id: ELEMENT_SKELETON}


def get_data(schema_id=None):
    #print(f'Schema ID: {schema_id}')
    return SCHEMA_SKELETON


query = """query ($id: Int){
                my_data(id: $id) {
                    elements{
                        id 
                        type_id 
                        display_name
                    }
                } 
            }
        """

mutation1 = """mutation 
                updateMutation($id: Int, $el_id: String, $update: String){
                    update_data(id: $id){
                            id
                            name
                            currency
                            elements{
                                id 
                                type_id 
                                display_name
                            }
                            dev{
                                element(el_id: $el_id){
                                    id
                                    type_id
                                    left
                                    params{
                                        currency{
                                            change
                                            value(val: $update)
                                        }
                                        s_in{value position(val: "BottomLeft")}
                                    }
                                }   
                          }
                     
                    }
                }
        """


mutation = """mutation($id: Int, $el_id: String, $update: String){
                   update_data(id: $id){
                            id
                            name
                            dev{
                                element(el_id: $el_id){
                                    type_id
                                    display_name(val: $update)
                                    left
                                    params{
                                        currency{
                                            change
                                            value(val: $update)
                                        }
                                        ma{
                                            value
                                        }
                                        s_in{value position(val: "BottomLeft")}
                                    }
                                }   
                            }
                     
                    }
    
                } 

        """


variables = {'id': 435456546, 'el_id': 'ma_val', 'update': 'EURUSD'}
context = {}



'''
#import collections
#from copy import deepcopy

# Immutable version
def merge(dict1, dict2):
    """ Return a new dictionary by merging two dictionaries recursively. """

    result = deepcopy(dict1)

    for key, value in dict2.items():
        if isinstance(value, collections.Mapping):
            result[key] = merge(result.get(key, {}), value)
        else:
            result[key] = deepcopy(dict2[key])

    return result


# Mutable version
def merge1(dict1, dict2):
    """ Updates dict1 recursively. """

    result = dict1 #deepcopy(dict1)

    for key, value in dict2.items():
        if isinstance(value, collections.Mapping):
            result[key] = merge(result.get(key, {}), value)
        else:
            result[key] = deepcopy(dict2[key])

    return result
'''


