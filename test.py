# -*- coding: utf-8 -*-
import collections
from copy import deepcopy
import graphene
from graphene import ObjectType, String, Schema, Field, Int, Boolean
import json
import data
from structure import FlowchartStructure as DataStructure # Use such alias for your schema

"""

Graphene usage to update and validate values of nested dictionary. Allow to update
corresponding fields during GraphQL standart query syntax.  

Your graphene object should be designed to define data strucrure and field types.
Import your object as `DataStructue` alias to avoid naming collision. 

A special middleware `StructureUpdate` allow to intercept field `args`, 
validate them and update corresponding key -> value of Data dict. 
If validation has failed - update will be skipped, and your data remains.
As a `Scalar` type is an endpoint of field resolving, `StructureUpdate` may utilize
`serialize` method of corresponding field to validate it's update value. 

"""


class NestingUpdate(object):
    """ Update nesting dict key - values during GraphQL field resolving

    The validation of incoming params must be implemented via defining
    Scalar based subclasses to allow  middleware utilize the `serialize` method
    to validate value for updated field

    """
    el_id = None         # This is specific only for TradingFlowcharts
    context_key = 'update'

    def create_update(self, my_path, update=""):
        """Generates dict with a depth to corresponding field,
        uses info.path to discover element nesting

        """
        if my_path.prev:
            key = my_path.key

            

            # This is specific only for TradingFlowcharts structure
            if key == 'element':
                key = self.el_id
            ###
            


            update = {key: update}
            return self.create_update(my_path.prev, update)
        return update

    def apply_update(self, data, update):
        """Updates data dict recursively by update dict, mutable method"""

        for key, value in update.items():

            if isinstance(value, collections.Mapping):
                data[key] = self.apply_update(data.get(key, {}), value)
            else:
                data[key] = deepcopy(update[key])

        return data

    def resolve(self, next, root, info, **args):
        """Provides data validation and structure update during resolving"""
      
        # Context must contain dict for update, otherwize -> skip this Middleware
        if not self.context_key in info.context:
            return next(root, info, **args)
                 
        # This requirement is specific for flowchart data structure and may be skipped
        if 'el_id' in args:
            self.el_id = args.get('el_id')
            return next(root, info, **args)  # Check this stuff later
        
        update_value = list(args.values()).pop() if args.values() else None

        # The narrow place here -> we have to destinguish update variable
        # because it may be passed as 0 or Null ???
        if update_value or update_value==0:     
            
            #print(f'>> Found kwargs argument {update_value}')

            # Scalar type is an endpoint of data resolving, so we may use it for validation            
            field = info.return_type             
            result = field.serialize(update_value) if hasattr(field, 'serialize') else update_value
           
            # Construct update
            update = self.create_update(info.path, result)
           
            # If no errors - update data structure
            try:
                self.apply_update(info.context.get(self.context_key), update)
            except Exception as e:
                #print(f'Failed to apply update {e}')    
                return next(root, info, **args)
                

            return result
            
        #print('\n')
        return next(root, info, **args)


# Deprecated
class UpdateNestingData(graphene.Mutation):
    """Provides nested data structure update

    This mutation provides nested dict data validation and  update
    during resolving of corresponding query. Standard GraphQL syntax and 
    variables should be used.
    
    Descripton:
        - Retriveves dict data (any method may be used)
        - Push data into `context`, to provide access for `StructureUpdate` middleware. 
            Notice: the same `context_key` should be used for mutation and middleware
            to destinguish your data.   
        - Init graphene Data object of your data, `DataStructure` alias is used for convenience  
        - Data object is binded to mutation `Output` to provide query resolving 

    """
    
    class Arguments:
        id = Int(required=True, description="The interenal ID to distinguish your data")
        context_key = String(default_value='update')

    Output = DataStructure
    
    def mutate(self, info, id, context_key, **kwargs) :
    
        # Get your data, use external function for convenience of refactoring
        my_data = data.get_data(id)  
        
        # Push data into context to prorvide access for middleware
        info.context.update({context_key: my_data})

        # Init and return Graphene object, use `DataStructure` alias for convenience
        return DataStructure(**my_data)


class AddElement(graphene.Mutation):
    """Add flowchart element"""

    class Arguments:
        type_id = Int(required=True, description="Flowchart element type_id")
    
    success = Boolean(default_value=False) 
    json_data = String() 

    def mutate(self, info, type_id, context_key='update', success=False) :

        """
        Todo:
            - test for empty data is required
            - test for error during data resolvinng is required
        """

        # Get your data from context
        my_data = info.context.get(context_key)  
        
        # Retrieve element's data using external function for convenience
        element = data.new_element(type_id)
        
        # Apply element to data `dev` section  
        if element:
            my_data['dev'].update(element) 
            success = True
       
        # Push data back into context
        info.context.update({context_key: my_data})
        
        return AddElement(success=success, json_data=json.dumps(element)) 


class DelElement(graphene.Mutation):
    """Delete flowchart element"""

    class Arguments:
        el_id = String(required=True, description="Flowchart element id")
    
    success = Boolean(default_value=False) 
    
    def mutate(self, info, el_id, context_key='update', success=False) :
    
        # Get your data from context
        my_data = info.context.get(context_key)  
        
        # Retrieve element's data, use external function for convenience
        element = my_data['dev'].get(el_id, None)
        
        # Remove elemeent if exists 
        if element:
            del my_data['dev'][el_id] 
            success = True
        
        # Push data back to context
        info.context.update({context_key: my_data})
        return DelElement(success=success) 


class Mutations(ObjectType):
    #update_data = UpdateNestingData.Field()
    add_element = AddElement.Field()
    del_element = DelElement.Field()
    #enable = EnableFlowchart.Field()  # Todo
    #run = RunFlowchart.Field()        # Todo
                 

class Query(ObjectType):

    my_data = Field(DataStructure, id=Int(required=True, description="The interenal ID to distinguish your data"))
    
    def resolve_my_data(root, info, id, data_key='update', **args):
        data = info.context.get(data_key, None)
        return DataStructure(**data)


if __name__=='__main__':
    """Usage example

   Update DATA_SAMPLE dict during the querying of corresponding fields. 
   The position of updated field is defined by query structure, field value 
   may be placed in `variables` or hardcoded directly in query. 
   If no args be defined for the field - existing dict value will be resolved. 

   is will be discovered 

   Updates DATA_SAMPLE dict `ma`, `s_in`,  

    """    

    query = """query($el_id: String, $update: String) {
                    my_data {
                            id
                            name
                            currency(val: $update)                                   )
                            dev {
                                element(el_id: $el_id) {
                                    type_id
                                    display_name(val: $update)
                                    left
                                    params {
                                        currency {
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
    variables = {'el_id': 'ma_val', 'update': 'EURUSD'}
    context = {'update': data.DATA_SAMPLE}
    schema = Schema(query=Query, mutation=Mutations, auto_camelcase=False)
    result = schema.execute(query, middleware=[NestingUpdate()], variables=variables, context=context)
    print(json.dumps(result.data, sort_keys=False, indent=4))
    




        