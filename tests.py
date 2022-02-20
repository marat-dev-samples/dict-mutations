"""'
Tests for TradingFlowchart params validation and update using Graphene 
useful for debugging and code refactoring
- put existing schema in setup for this tests 
- test params (dates) must be configured according with servers rates ability for this dates

Run this tests using: 
- python -m unittest -v tests.ibkrbot_tests

"""

import unittest
from collections import namedtuple
import copy
import graphene
from graphene.test import Client
import json
from test import Query, NestingUpdate, DATA_KEY
import data


class NestingUpdateTests(unittest.TestCase):
    
    def setUp(self):
        self.schema = graphene.Schema(query=Query, mutation=graphene.Mutations, auto_camelcase=False)
        self.data = data.DATA_SAMPLE
        self.context_key = DATA_KEY

    def test_restricted_fields(self):
        """Test for attempt to change restricted field value
        
        Used request contained all restricted fields ??? 
        
        Fields:
            id
            dev -> element -> type_id

        Expected:
            - An empty data must be returned
            - The number of errors must be equal to amount of queried fields

        """
        variables = {'el_id': 'ma_val'}
        context = {self.context_key: self.data}
        query = """query($el_id: String){
                        my_data {
                            id(val: 1234567)
                            dev {
                                element(el_id: $el_id) {
                                    type_id(val: 123456)
                                    
                                }   
                            }
                    }
                } 
        """
        result = self.schema.execute(query, variables=variables, context=context)
        self.assertEqual(result.data, None, f'Restricted params data must returns Null result')
        self.assertEqual(len(result.errors), 2, f'The number of errors must be equal to amount of queried fields')

    def test_custom_scalars(self):
        """Test custom defined scalars for correct values

        For  

        ++ MA select                  1-255 -> rename to Smooth
        ++ Period select              5, 15, 60, 240
        ++ Available currency         ['GBPUSD', 'EURUSD']
        -- On/off                     ['on', 'off']  
        -- type_id (module name)      1-100000000 
        -- position                   ['TopCenter', 'BottomLeft'] 
        ++ Short name (Param name) String lengh 30 symbols, replace all excluding A-Z, a-z, 0-9, '+-=<>@$:;,.!?' 
        -- Long name (Flowchart name) String lengh 30 symbols, replace all excluding A-Z, a-z, 0-9, '+-=<>@$:;,.!?' 
   
        top, left -> int positive

        """

        base_variables = {'el_id': 'ma_val', 'ma_value': 2}
        context = {self.context_key: self.data}
        mutation = """query($el_id: String, $ma: Int, $currency: String, $period: Int, $display: String){
                        my_data {
                            id
                            currency(val: $currency)
                            dev {
                                element(el_id: $el_id) {
                                    display_name(val: $display)
                                    params {
                                        ma {
                                            value(val: $ma)
                                        }
                                        period {
                                            value(val: $period)
                                        }
                                        currency {
                                            value(val: $currency)
                                        }
                                    }    
                                }   
                            }
                    }
                } 
        """
        
        TestParams = namedtuple('TestParams', ['name', 'variable', 'values', 'result'])
        test_cases = [                      
            TestParams('Incorrect _Smooth value', 'ma', [0, -1, 256, 2.5, 'z'], False), 
            TestParams('Correct _Smooth value', 'ma', [1, 255], True), 
            TestParams('Incorrect _Quote', 'currency', ['USSGPY'], False), 
            TestParams('Correct _Period', 'period', [5, 15, 60, 240], True), 
            TestParams('Incorrect _Period', 'period', ['5', 0, 1, 1.5], False), 
            TestParams('Correct _ShortString', 'display', ['Moving averange 1'], True), 
            TestParams('Correct _ShortString', 'display', [f'Moving averange {"s"*30}', f'Moving @'], False), 
            
        ]
        for test in test_cases:
            
            for value in test.values: 
                #print(f'>>> {test.name}')
                variables = copy.deepcopy(base_variables) #.update({test.variable: test.value})
                variables.update({test.variable: value})
                print(variables)
                result = self.schema.execute(mutation, middleware=[NestingUpdate()], variables=variables, context=context)
                self.assertEqual(result.errors is None, test.result, f'Error {test.name}: {value} \n {result.errors}')

    def test_query(self):
        variables = {'el_id': 'ma_val', 'update': 'EURUSD'}
        context = {self.context_key: self.data}
        query = """query($el_id: String, $update: String) {
                    my_data {
                            id
                            name
                            dev{
                                element(el_id: $el_id) {
                                    type_id
                                    display_name(val: $update)
                                    left
                                    params {
                                        currency {
                                            change
                                            value(val: $update)
                                        }
                                        ma {
                                            value(val: 55)
                                        }
                                        s_in{value position(val: "BottomLeft")}
                                    }
                                }   
                            }
                     
                    }
    
                } 

        """
        result = self.schema.execute(query, middleware=[NestingUpdate()], variables=variables, context=context)
        
        print('i am here')

        print(json.dumps(result.data, sort_keys=False, indent=4))
        print(result.errors[0]) if result.errors else 'Success'

        # Check if data has changed
        #print(json.dumps(self.data, sort_keys=False, indent=4))








































