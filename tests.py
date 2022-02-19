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
from test import Query, Mutations, NestingUpdate
import data


class SecurityTestCases(unittest.TestCase):
    
    def setUp(self):
        self.schema = graphene.Schema(query=Query, mutation=Mutations, auto_camelcase=False)
        self.data = data.SCHEMA_SKELETON
        self.context_key = 'update'

    """
    def make_query(self, request, variables, context={}):
            schema = graphene.Schema(query=Query, mutation=Mutations, auto_camelcase=False)
            result = schema.execute(request, middleware=[StructureUpdate()], variables=variables, context=context)
            return result        
    """

    @unittest.skip("Test is skipped temporary")
    def test_restricted_fields(self):
        """Test changing restricted fields during mutation
        
        For this test request must contain all restricted fields 
        
        Fields:
            Schema -> id
            Schema -> dev -> element -> type_id

        Expected:
            - An empty data must be returned
            - The number of errors must be equal to count of restricted fields

        """
        variables = {'id': 435456546, 'el_id': 'ma_val'}
        context = {}
        mutation = """mutation($id: Int, $el_id: String){
                    update_data(id: $id){
                            id(val: 1234567)
                            dev{
                                element(el_id: $el_id){
                                    type_id(val: 123456)
                                    
                                }   
                            }
                    }
                } 
        """
        result = self.schema.execute(mutation, variables=variables, context=context)
        self.assertEqual(result.data, None, f'Restricted params data must returns Null result')
        self.assertEqual(len(result.errors), 2, f'Restricted param has changed, check result errors for details')

    @unittest.skip("Test is skipped temporary")
    def test_custom_scalars(self):
        """Test custom scalars values

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

        base_variables = {'id': 435456546, 'el_id': 'ma_val', 'ma_value': 2}
        context = {}
        mutation = """mutation($id: Int, $el_id: String, $ma: Int, $currency: String, $period: Int, $display: String){
                    update_data(id: $id){
                            id
                            currency(val: $currency)
                            dev{
                                element(el_id: $el_id){
                                    display_name(val: $display)
                                    params{
                                        ma{value(val: $ma)}
                                        period{value(val: $period)}
                                        currency{value(val: $currency)}
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

    @unittest.skip("Test is skipped temporary")
    def test_mutation(self):
        """Deprecated, use it to create and delete elemnets""" 

        variables = {'id': 435456546, 'el_id': 'ma_val', 'update': 'EURUSD'}
        context = {self.context_key: self.data}
        mutation = """mutation($id: Int, $el_id: String, $update: String){
                
                    update_data(id: $id) {
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
        result = self.schema.execute(mutation, middleware=[NestingUpdate()], variables=variables, context=context)
        print(json.dumps(result.data, sort_keys=False, indent=4))
        #print(result.errors)

        # Check if data has changed
        print(json.dumps(get_data(34545), sort_keys=False, indent=4))

    #@unittest.skip("Test is skipped temporary")
    def test_add_element(self):
        """Adding element to Flowchart

        Todo 
            use assert for both add and delete methods

        """ 

        variables = {'type_id': 750}
        context = {self.context_key: self.data}
        mutation = """mutation($type_id: Int){
                        add_element(type_id: $type_id) {
                            success
                            json_data
                        }    
                } 

        """
        result = self.schema.execute(mutation, middleware=[NestingUpdate()], variables=variables, context=context)
        print(json.dumps(result.data, sort_keys=False, indent=4))
        print(result.errors)

        # Check if data has changed, use assert here
        #print(json.dumps(self.data, sort_keys=False, indent=4))
 

    #@unittest.skip("Test is skipped temporary")
    def test_del_element(self):
        """Delete element from Flowchart""" 

        variables = {'el_id': 'ma_val'}
        context = {self.context_key: self.data}
        mutation = """mutation($el_id: String){
                        del_element(el_id : $el_id) {
                            success
                        }    
                } 

        """
        result = self.schema.execute(mutation, middleware=[NestingUpdate()], variables=variables, context=context)
        print(json.dumps(result.data, sort_keys=False, indent=4))
        print(result.errors)

        # Check if data has changed, use assert here
        #print(json.dumps(self.data, sort_keys=False, indent=4))
         








    
    @unittest.skip("Test is skipped temporary")
    def test_query(self):
        variables = {'id': 435456546, 'el_id': 'ma_val', 'update': 'EURUSD'}
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
        print(json.dumps(result.data, sort_keys=False, indent=4))
        
        # Check if data has changed
        #print(json.dumps(self.data, sort_keys=False, indent=4))








































