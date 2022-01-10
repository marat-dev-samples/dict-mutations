# -*- coding: utf-8 -*-


import graphene
from graphene import ObjectType, String, Schema, Field, List
from graphene import ID
from graphene.types import Scalar
import json

from data import *

from graphene.types.resolver import dict_resolver


Data = {}


'''
class UserType(DjangoObjectType):

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
            'email',
            'first_name',
            'last_name',
            'is_active',
            'group_ids',
        )

    full_name = graphene.String()           # Python property
    full_identification = graphene.String() # Python property


- Updating of element
- check if elementt exists by id
- dynamycally load fields from existing schema element !!!
- update element's data from kwargs

in Mutation it provides element data only -> retrieve element id
in Mutation you should receive element by id and then save

'''



"""Custom Scalars"""

class ShortString(Scalar):
    
    myformat = String(default_value='')

    @staticmethod
    def serialize(s):
        print(f'i am short string resolver')
        return f'ShortString {s}'


class PeriodSelect(Scalar):
    
    @staticmethod
    def serialize(s):
        periods = ['5', '15', '60', '240']
        if s not in periods:
            return False
        print(f'i am resolver')
        return f'{s} ------ S'


class _Quotes(Scalar):

    @staticmethod
    def serialize(s):
        values = AVAILABLE_QUOTES
        if s not in values:
            print(f'>>>>>>>>>>>>>Error currency {s}')
            raise Exception('Incorrect currency param')
        print(f'i am currency serializer {s}')
        return f'{s} ------ S'



# Element beginning
'''
class FlowchartElement(graphene.Interface):
    id = graphene.ID(required=True, default_value='1')
    display_name = graphene.String(required=True, default_value='element1')
    type_id = graphene.String(required=True, default_value='None')
    top = graphene.Int(required=True, default_value=0)
    left = graphene.Int(required=True, default_value=880)
    #params = graphene.ObjectType
'''


"""Element params"""

class ElementParam(graphene.Interface):
    id = String()                               # Restricted for changing 
    display_name = String(default_value='')     
    change = String(default_value='text')       # Restricted for changing
    info_arr = String(default_value='sensor')   # You can't change this param

    def resolve_display_name(root, info, display_name='', **kwargs):
        return display_name


class StringParam(ObjectType):
    class Meta:
        interfaces = (ElementParam, )
    value = String(default_value='') 


class MaSelect(ObjectType):
    class Meta:
        interfaces = (ElementParam, )
    
    value = Field(String) # Available currency
 
    def resolve_value(root, info, value='', **kwargs):
         return value


class CurrencySelect(ObjectType):
    class Meta:
        interfaces = (ElementParam, )
    
    change = String()       # Available change
    value = Field(_Quotes)   # Available currency
    #value = Field(ListValue, to=String(default_value='i am here')) # Available currency
    #value = Currency()

    def resolve_change(root, info, change='', **kwargs):
        return change

    '''
    def resolve_value(root, info, value='', **kwargs):
        print(kwargs)
        return value
    '''



"""Element definition"""



class Params(ObjectType):
    """List all available elements params here"""
    l_in = Field(StringParam)   # define short string, currency param #graphene.String(required=True, default_value='')
    l_out = Field(StringParam)   #graphene.String(required=True, default_value='')
    s_in = Field(StringParam)   #graphene.String(required=True, default_value='')
    s_out = Field(StringParam)  #graphene.String(required=True, default_value='')
    #ma = Field(MaSelect) 
    # period
    currency = Field(CurrencySelect) 

    # Deprecated        
    #@classmethod 
    #def get_param(self, name):
    #    print('--------Get param-----------')
    #    param = getattr(self, name)
    #    return param.type



class Element(ObjectType):
    """Flowchart element common structure"""
    
    #class Arguments:
    #    display_name = String()

    id = graphene.String(required=True, default_value='')
    display_name = graphene.String(required=True)
    top = graphene.Int(required=True, default_value=0)
    left = graphene.Int(required=True, default_value=880)
    type_id = Field(ShortString) 
    params = Field(Params)

    def resolve_type_id(root, info, type_id='', **kwargs):
        return type_id

    #def resolve_display_name(root, info, display_name='', **kwargs):
    #    return display_name


    '''  
    @staticmethod
    def update_param(self, name, field, value):
        print(f'> Update {name} -> {field} -> {value}')
        # Retrieve subclass class of certain param
        param_class = Params.get_param(name)
        param_class.validate(field, value)
        # If no errors -> change param value
        self.params[name]['value'] = value
    '''    




class _Dev(ObjectType):
    
    element = Field(Element, el_id=String())  
    
    def resolve_element(root, info, el_id, **kwargs):
        #el_id = "ma_val"
        print(el_id)
        el_data = SCHEMA_SKELETON['dev'][el_id]
        return Element(**el_data)
    

class FxSchema(ObjectType):
    """Flowchart schema common structure"""
    
    id = String(required=True)            # Restricted
    name = String(required=True)          
    enable = String(required=True)        
    currency = String(required=True)       
    datetime = String()  
    dev = Field(_Dev, el_id=String())                  

    



    def resolve_name(root, info, name='', **kwargs):
        return name



    





class ValidationMiddleware(object):

    current = dict()
    current_element = ''


    def update_by_path(self, dict1, my_path, update=""):
        #print(type(my_path))
        #print(my_path)
        print(f'>>> path {my_path.key}')


        if my_path.prev:
        
            key = my_path.key
            if key == 'element':
                key = 'ma_val' 

            update = {key: update}        
    
            return self.update_by_path(dict1, my_path.prev, update)
        else:
            print(update)
            return update


    def resolve(self, next, root, info, **args):
        
        """You may use context `update` internally dict for update values"""

        #dict_obj = SCHEMA_SKELETON['dev']["ma_val"]["params"].get('currency')
        field = info.field_name
        print(f'> Validation {field}') 
        #print(f'{self.current}')     
        #self.current = info.path 
        #print(f'{self.current}')     
        

        '''
        if root:
            print(root) 
            try:
                print(f'>{root.get(field, "")}')
            except Exception as e:
                print(e)


            try:
                print(f'>{getattr(root, field)}')
            
            except Exception as e:
                print(e)
        '''

        

        update_value = info.context.get(field, None)
        if update_value:
            print(f'> Found update value {update_value}')
            update = self.update_by_path(SCHEMA_SKELETON, info.path, update_value)
            #self.current = merge1(self.current, update) 


        #if field == 'currency':
        #    dict_obj['value'] = 'EURUSD'

 

        '''
        if field in info.context:
            args.update({field: info.context[field]})
        
        elif type(root) == dict:
            args.update({field: root.get(field, "")})
        
        elif hasattr(root, '__dict__'):
            if field in root.__dict__:
                args.update({field: root.__dict__.get(field, "z")})
        '''

        #print(f'> update {args}')



        print('\n')
        
        '''
        elif type(root) == dict:
            args.update({field: root.get(field, "")})
        '''

        #print(json.dumps(self.current, indent=4))


        return next(root, info, **args)        


"""Mutations"""

class UpdateElement(graphene.Mutation):

    """Updates flowchart element

    This method must accept element id and init element's data 
    Updating process uses ValidationMiddleware to push values from context to kwargs
    and further resolving of updated param. Allow to update multiple params (uniqie)
    with deep nesting.
    """
 
    class Arguments:
        el_id = String(default_value='') 
    
    element = Field(Element, el_id=String())
    
    def mutate(self, info, el_id='', **kwargs):
        el_data = SCHEMA_SKELETON['dev'].get(el_id, dict())
        if not el_data:
             raise Exception(f'Element {el_id} not found')
        element = Element(**el_data)
        return UpdateElement(element=element)


class UpdateFlowchart(graphene.Mutation):
    
    # List params that is allowable to update
    class Arguments:
        schema_id = String(default_value='')
    #    el_data = String()
      
    # Response fields
    print('> Call update schema')
    data = Field(FxSchema)

    #class Meta:
    #    output = self.result

    def mutate(self, info, **kwargs) :
        print('>>> Update flowchart')
        data = FxSchema(**SCHEMA_SKELETON)
        return UpdateFlowchart(data=data)


class Mutations(ObjectType):
    update_element = UpdateElement.Field()
    update_flowchart = UpdateFlowchart.Field()


"""Query"""

class Query(ObjectType):
    name = String()
    enable = String()
    dev = Field(Element)
    
    def resolve_name(root, info, n):
        return info.context.get('name')


    def resolve_enable(root, info):
        return 'off' 

    '''
    def resolve_dev(root, info):
        #print(f'i am resolver')
        return Element()
        #return {'el_id':'R2', 'el_name':'D2', 'el':'None', 'el1':'None'}
        #return #ObjectType 
        #return Element() #ObjectType {}
    '''



schema = Schema(query=Query, mutation=Mutations, auto_camelcase=False)
result = schema.execute(query, root=SCHEMA_SKELETON, middleware=[ValidationMiddleware()], variables=variables, context=context)
#result = schema.execute(query, variables=variables, context=context)


#print(result.data.get('update_element'))

'''
update = result.data.get('update_element')
if update:
    
    el_data = update.get('element')
    if el_data:
        el_id = el_data.get('id')
        update_data = {"dev": {el_id: el_data}}
        result = merge1(SCHEMA_SKELETON, update_data)
        print(json.dumps(result, sort_keys=False, indent=4))
 
'''


# If update query -> update result ???
# But if not, how can we filter that

print(json.dumps(result.data, sort_keys=False, indent=4))
print(result.errors)


#query = 'mutation myFirstMutation {addElement(name:"s_in2"){element {id displayName typeId}}}'
#result = schema.execute(query, root=Data)


#print(Data)