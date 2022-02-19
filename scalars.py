import graphene
from graphene import ObjectType, String, Field, String, Schema, Field, List

from graphene.types import Scalar


# Replace with method
AVAILABLE_QUOTES = ['GBPUSD', 'EURUSD']




"""Custom Scalars"""
class _ShortString(Scalar):
    
    myformat = String(default_value='')

    @staticmethod
    def serialize(s):
        print(f'i am short string resolver')
        return f'ShortString {s}'


class _Quote(Scalar):
    """Available quote, may vary for different servers, use from  list of quotes"""

    @staticmethod
    def serialize(val):
        print(f'>>> Call serialize quotes {val}')
        if val not in AVAILABLE_QUOTES:
            raise Exception(f'Incorrect currency param {val}')
        return val
    

class _Period(Scalar):
    """Available period of data, should be in list (5, 15, 60, 240) """

    @staticmethod
    def serialize(val):
        print(f'>>> Call serialize period {val}')
        if val not in ['5', '15', '60', '240']:
            raise Exception('Incorrect peirod param')
        return val
    
    
class _Smooth(Scalar):
    """Available smooth for line indicator like Moving averange, e.t.c. 
    Must be an integer value in range 1-255

    """
    @staticmethod
    def serialize(val):
        print(f'>>> Call serialize smooth {val}')
        if val not in range(1, 255):
            raise Exception('Incorrect smooth param')
        return val


class _LinePosition(Scalar):
    """Available position for Flowchart line ancor or endpoint"""

    @staticmethod
    def serialize(val):
        if val not in ['TopCenter', 'BottomLeft', 'MiddleLeft', 'MiddleRight']:
            raise Exception(f'Incorrect position param {val}')
        return val


"""Element params are based on common Param interface"""
class Param(graphene.Interface):
    id = String()                               # Restricted for change 
    display_name = Field(String, val=String())  # Allowable for change
    
    change = String()                           # Restricted for change
    info_arr = String(default_value='sensor')   # You can't change this param
    position = Field(_LinePosition, val=String())
    

class StringParam(ObjectType):
    class Meta:
        interfaces = (Param, )
    value = String(default_value='') 


class SmoothSelect(ObjectType):
    class Meta:
        interfaces = (Param, )
    #change = String()
    value = Field(_Smooth, val=String())    # This field is abailable for changing


# Param cirrency select
class CurrencySelect(ObjectType):
    
    class Meta:
        interfaces = (Param, )
    change = String()                        # This field has no args, it's not available for changing
    value = Field(_Quote, val=String())    # This field is abailable for update
    

# Param period select
class PeriodSelect(ObjectType):
    
    class Meta:
        interfaces = (Param, )
    
    value = Field(_Period, val=String())    # This field is abailable for changing
    

"""Structure Definition"""
class ElementParams(ObjectType):
    """List all available params here"""
    l_in = Field(StringParam)   # define short string, currency param #graphene.String(required=True, default_value='')
    l_out = Field(StringParam)   #graphene.String(required=True, default_value='')
    
    s_in = Field(StringParam)   #graphene.String(required=True, default_value='')
    s_out = Field(StringParam)  #graphene.String(required=True, default_value='')
    

    ma = Field(SmoothSelect) 
    # period
    
    # List all available params here
    currency = Field(CurrencySelect) 
    period = Field(PeriodSelect)
    

class Element(ObjectType):
    """Flowchart element common structure"""
    
    id = graphene.String(required=True, default_value='')
    display_name = graphene.String()
    top = graphene.Int(required=True, default_value=0)
    left = graphene.Int(required=True, default_value=880)
    type_id = Field(_ShortString) 
    params = Field(ElementParams)


class _Dev(ObjectType):
    
    element = Field(Element, el_id=String())  
    
    def resolve_element(root, info, el_id, **kwargs):
        el_data = root.get(el_id)
        #el_data = SCHEMA_SKELETON['dev'][el_id]    # Bug here !!!
        return Element(**el_data)
    

class DataStructure(ObjectType):
    """Flowchart schema common structure"""
    
    id = String(required=True)            # Prohibited
    name = String(required=True)          
    enable = String(required=True)        
    currency = String(required=True)       
    datetime = String()  
    dev = Field(_Dev, el_id=String())                  
    elements = List(Element)

    
    def resolve_elements(root, info, **kwargs):
        return [Element(**el_data) for el, el_data in root.dev.items()]
