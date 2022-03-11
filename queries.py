# -*- coding: utf-8 -*-
import collections
from copy import deepcopy
from graphene import ObjectType, Field, Int

# Import data type object with `DataStructue` alias to avoid naming collision. 
from data_types import NestedStructure as DataStructure 

# This key is common for middleware and queryes
DATA_KEY = 'update'


class NestingUpdate(object):
    """ Update nesting dict values during GraphQL field resolving

    As a `Scalar` type is an endpoint of field resolving, 
    `NestingUpdate` may utilize `serialize` method of corresponding field 
    to validate it's update value. 

    """
    el_id = None             # This is specific only for `Flowcharts` structure
    context_key = DATA_KEY

    def create_update(self, my_path, update=""):
        """Generates dict according to the field nesting. 
        
        Utilizes info.path to discover element nesting

        """
        if my_path.prev:
            key = my_path.key
            # This is specific only for `Flowcharts` data structure
            if key == 'element':
                key = self.el_id
            #            
            update = {key: update}
            return self.create_update(my_path.prev, update)
        return update

    def apply_update(self, data, update):
        """Updates dict recursively with another dict. Mutable method"""

        for key, value in update.items():
            if isinstance(value, collections.Mapping):
                data[key] = self.apply_update(data.get(key, {}), value)
            else:
                data[key] = deepcopy(update[key])
        return data

    def resolve(self, next, root, info, **args):
        """Provides data validation and structure update during resolving"""
      
        # Context must contain data dict, otherwize -> skip update
        if self.context_key not in info.context:
            return next(root, info, **args)
        
        # No update, resolve field value         
        if not args:
            return next(root, info, **args)
        
        # This feature is specific for flowchart project and may be omitted
        if 'el_id' in args:
            self.el_id = args.get('el_id')
            return next(root, info, **args)

        if not args:
            return next(root, info, **args)

        # Retrieve and validate input value            
        update_value = list(args.values()).pop() 
        field = info.return_type             
        result = field.serialize(update_value) if hasattr(field, 'serialize') else update_value
        
        # Construct update dict and apply to data 
        update = self.create_update(info.path, result)
        try:
            self.apply_update(info.context.get(self.context_key), update)
        except Exception:
            return next(root, info, **args)
        return result
        

class Query(ObjectType):
    my_data = Field(DataStructure)
    
    def resolve_my_data(root, info, data_key=DATA_KEY, **args):
        data = info.context.get(data_key, None)
        return DataStructure(**data)
