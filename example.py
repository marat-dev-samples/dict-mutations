# -*- coding: utf-8 -*-
"""This is an example of Graphene utilization to update nested dictionary.

Update is processed during GraphQL query. The position of updated fields 
is defined by query structure.  

A special middleware `StructureUpdate` is designed to intercept field `args`, 
validate them and update corresponding item in DATA dict. 
If validation of input value has failed - update will be skipped, and your data remains.

Your graphene object should be designed to define data structure and field types.
As a `Scalar` type is an endpoint of field resolving, `StructureUpdate` utilized
`serialize` method of corresponding field to validate input value. 
Python -V > 3.7.2
"""

import json
import graphene
from queries import Query, NestingUpdate, DATA_KEY


# Create schema
my_schema = graphene.Schema(query=Query, auto_camelcase=False)

# Nested dict sample
DATA = {
    'id': '123456789',            
    'name': 'Sample of elements settings',
    'currency': 'GBPUSD',
    'dev': {
            'element1': {
                'id': 'element1',
                'type_id': '550', 
                'params': {
                    'currency': {
                        'value': 'GBPUSD'
                    },
                    'period': {
                        'value': 15, 
                    }, 
                }
            },
            'element2': {
                'id': 'element2',
                'type_id': '570', 
                'params': {
                    'currency': {
                        'value': 'GBPUSD'
                    },
                    'period': {
                        'value': 60, 
                    }, 
                }
            }
    }    
}

if __name__== '__main__':
    """Usage example

    Updates DATA_SAMPLE dict during the querying of corresponding fields. 
    The position of updated field is defined by query structure, update value 
    may be placed in `variables` or hardcoded directly in a query. 
    If no args are provided for the field - existing key value will be resolved. 
    
    """    

    # Implement query to update nested key
    query = """query($el_id: String, $update: String, ) {
                    my_data {
                            currency(val: $update)
                            dev {
                                element(el_id: $el_id) {
                                    type_id
                                    params {
                                        currency {
                                            value(val: $update)
                                        }
                                        period {
                                            value(val: 240)
                                        }
                                    }
                                }   
                        }
                }
            } 
    """
    variables = {'el_id': 'element2', 'update': 'EURUSD'}
    
    # Put DATA into context with DATA_KEY to provide access for middleware
    context = {DATA_KEY: DATA}
    
    # Execute query with `NestingUpdate` middleware
    result = my_schema.execute(query, middleware=[NestingUpdate()], 
                               variables=variables, context=context)
    
    # Print output
    print(json.dumps(result.data, sort_keys=False, indent=4))
    print(result.errors) if result.errors else print('Success')
    
    # Check result
    updated_val = DATA.get('dev').get('element2').get('params').get('currency').get('value')
    assert updated_val == 'EURUSD'