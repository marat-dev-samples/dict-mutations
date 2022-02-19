import graphene
from graphene import InputObjectType, ObjectType, String, Field, String, Int, Field, List
from graphene.types import Scalar
import re


# Replace with method
AVAILABLE_QUOTES = ['GBPUSD', 'EURUSD']

"""Custom Scalars"""
class _ShortString(Scalar):
    """Short string commonly used for displaying param name or current state"""
    
    @staticmethod
    def serialize(val):
        n = 30
        if len(val) > n:
            raise Exception(f'Too long string param: `{val}` must be less then {n} symbols')
        
        #date_str = re.sub(r'[^0-9-:\s]', '', date_str)     # Remove any non digatals symbols, exclude delimiters
        if re.search(r'[^a-zA-z0-9-:=]+$', val):
            raise Exception(f'Not valid string param: `{val}` do not use specific symbols')
        
        return val


class _Quote(Scalar):
    """Available quote, may vary for runned servers, use defined list of quotes"""

    @staticmethod
    def serialize(val):
        if val not in AVAILABLE_QUOTES:
            raise Exception(f'Incorrect currency param {val}')
        return val
    

class _Period(Scalar):
    """Available period of data, should be in list (5, 15, 60, 240) """

    @staticmethod
    def serialize(val):
        if val not in [5, 15, 60, 240]:
            raise Exception('Incorrect peirod param')
        return val
    
    
class _Smooth(Scalar):
    """Available smooth for line indicator like Moving averange, e.t.c. 
    Must be an integer value [1-255]

    """
    @staticmethod
    def serialize(val):
        if val not in range(1, 256):
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
    value = Field(_Smooth, val=Int(), default_value=1, required=True)    # This field is abailable for changing


# Param cirrency select
class CurrencySelect(ObjectType):
    """Quote selection param"""
    class Meta:
        interfaces = (Param, )
    change = String()                                      # Restricted
    value = Field(_Quote, val=String())    
    

# Param period select
class PeriodSelect(ObjectType):
    
    class Meta:
        interfaces = (Param, )
    
    value = Field(_Period, val=Int())    # This field is abailable for changing
    

"""Structure Definition"""
class ElementParams(ObjectType):
    """List all available params here"""
    
    # Line params
    l_in = Field(StringParam)   # define short string, currency param #graphene.String(required=True, default_value='')
    l_out = Field(StringParam)   #graphene.String(required=True, default_value='')
    s_in = Field(StringParam)   #graphene.String(required=True, default_value='')
    s_out = Field(StringParam)  #graphene.String(required=True, default_value='')
    l_info = Field(StringParam)   #graphene.String(required=True, default_value='')
    

    # List all available params here
    period = Field(PeriodSelect)
    currency = Field(CurrencySelect) 
    ma = Field(SmoothSelect) 
    

class Element(ObjectType):
    """Flowchart element common structure"""
    id = String(required=True)                             # Restricted
    display_name = Field(_ShortString, val=String())
    top = Field(Int, default_value=0, val=Int())            
    left = Field(Int, default_value=880, val=Int())        
    type_id = Field(_ShortString)                          # Restricted, validate existing 
    params = Field(ElementParams)


class _Dev(ObjectType):
    
    element = Field(Element, el_id=String())  
    
    def resolve_element(root, info, el_id, **kwargs):
        el_data = root.get(el_id)
        return Element(**el_data)
    

class FlowchartStructure(ObjectType):
    """Flowchart schema common structure"""
    
    id = String(required=True)            # Prohibited
    name = String(required=True)          
    enable = String(required=True)        
    currency = Field(_Quote, val=String())    
    datetime = String()  
    dev = Field(_Dev, el_id=String())                  
    elements = List(Element)

    
    def resolve_elements(root, info, **kwargs):
        return [Element(**el_data) for el, el_data in root.dev.items()]







