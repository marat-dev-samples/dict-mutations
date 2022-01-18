

AVAILABLE_QUOTES = ['GBPUSD', 'EURUSD']





SCHEMA_SKELETON = {
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
                's_in': {'id': 's_in', 'display_name': 'MA value', 'position': 'TopCenter', 'info_arr': 'sensor', 'value': 1.0},
                's_out': {'id': 's_out', 'display_name': 'MA value', 'position': 'TopCenter', 'info_arr': 'sensor', 'value': 0.0},
                'currency': {'id': 'currency', 'display_name': 'Currency', 'change': 'currency_select', 'value': 'GBPUSD'},
    
           }
        }
    }    
}


SKELETON1 = {
    'id': 'ma_val',
    'display_name': 'Moving averange', 
    'type_id': '550', 
    'top': None , 
    'left': None,
    'params': {
        'ma': {'value': 0, 'display_name': 'MA set', 'id': 'ma', 'change': 'text'},
        'period': {'id': 'period', 'display_name': 'Period set', 'value': '', 'change': 'period_select'}, 
        'currency': {'id': 'currency', 'display_name': 'Currency', 'change': 'currency_select', 'value': ''},
        's_out': {'id': 's_out', 'display_name': 'MA value', 'position': 'TopCenter', 'info_arr': 'sensor', 'value': 0.0}
    } 
}

SKELETON = {
    'id': 'ma_val',
    'display_name': 'Moving averange', 
    'type_id': '550', 
    'top': 0, 
    'left': 550,
    'params': {
         's_in': {'id': 's_in', 'display_name': 'MA value', 'position': 'TopCenter', 'info_arr': 'sensor', 'value': 1.0},
         's_out': {'id': 's_out', 'display_name': 'MA value', 'position': 'TopCenter', 'info_arr': 'sensor', 'value': 0.0},
         'currency': {'id': 'currency', 'display_name': 'Currency', 'change': 'currency_select', 'value': 'GBPUSD'},
    
    }
}







query1 = """mutation 
               myFirstMutation{
                    update_element(el_id:"s_in1"){
                        data{
                            id
                            type_id
                            left
                            params{
                                currency{
                                   value
                                }
                                s_in{
                                   display_name
                                }
                            }
                        }
                    }
                }
        """

#context = {'value': 'USDRUB', 'display_name': 'New element'}
#context = {}

from graphene import ID


query1 = """mutation 
                flowchartMutation($el_id: String){
                    update_flowchart{
                        data{
                            id
                            name
                            currency
                            dev{
                                element(el_id: $el_id){
                                    id
                                    type_id
                                    left
                                    params{
                                        currency{value}
                                        s_in{display_name}
                                    }
                                }   
                            }
                        }
                    }
                    update_element(el_id: $el_id){
                        element{
                            id
                            type_id
                            left
                            params{
                                currency{
                                   value
                                }
                                s_in{
                                   display_name
                                }
                            }
                        }
                    }    
                    
                }
        """



query = """mutation 
                flowchartMutation($el_id: String){
                    update_flowchart{
                        data{
                            id
                            name
                            currency
                            dev{
                                element(el_id: $el_id){
                                    id
                                    type_id
                                    left
                                    params{
                                        currency{value}
                                        s_in{display_name}
                                    }
                                }   
                            }
                        }
                    }
                }
        """














context = {'name': 'New schema create', 'display_name': 'New name', 'value': 'EURUSD'}
variables = {'el_id': 'ma_val'}


import collections
from copy import deepcopy





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





"""
def update_by_path(dict1, my_path, update=""):
    #print(type(my_path))
    #print(my_path)
    print(f'>>> path {my_path.key}')


    if my_path.prev:
        
        key = my_path.key
        if key == 'element':
            key = 'ma_val' 

        update = {key: update}        
    
        return update_by_path(dict1, my_path.prev, update)
    else:
        print('ok')
        print(update)
        return update

"""        