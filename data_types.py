import graphene
from graphene import ObjectType, String, Field, Int, List
from graphene.types import Scalar
import re

AVAILABLE_QUOTES = ['GBPUSD', 'EURUSD']


class _ShortString(Scalar):
    """Short string, commonly used for displaying name"""
    
    @staticmethod
    def serialize(val):
        n = 30
        if len(val) > n:
            raise Exception(f'Too long string param: `{val}` must be less then {n} symbols')
        # Remove any non digatals symbols, exclude delimiters
        if re.search(r'[^a-zA-z0-9-:=]+$', val):
            raise Exception(f'Not valid string param: `{val}` do not use specific symbols')
        return val


class _Quote(Scalar):
    """Available quote, should be from defined list of quotes"""

    @staticmethod
    def serialize(val):
        if val not in AVAILABLE_QUOTES:
            raise Exception(f'Incorrect currency param {val}')
        return val
    

class _Period(Scalar):
    """Available period of data, should be integer from list of (5, 15, 60, 240) """

    @staticmethod
    def serialize(val):
        if val not in [None, 5, 15, 60, 240]:
            raise Exception('Incorrect period param')
        return val
    

class Param(graphene.Interface):
    """Interface for params which are common for all elements"""
     
    id = String()                               # Restricted
    display_name = Field(String, val=String())
    change = String()                           # Restricted
    info_arr = String(default_value='sensor')
    

class StringParam(ObjectType):
    class Meta:
        interfaces = (Param, )
    value = String(default_value='')


class CurrencySelect(ObjectType):
    """Quote selection param"""
    class Meta:
        interfaces = (Param, )
    change = String()                          # Restricted
    value = Field(_Quote, val=String())
    

class PeriodSelect(ObjectType):
    class Meta:
        interfaces = (Param, )
    value = Field(_Period, val=Int())
    

class ElementParams(ObjectType):
    """All available params of element"""
    
    period = Field(PeriodSelect)
    currency = Field(CurrencySelect)
    

class Element(ObjectType):
    """Flowchart element structure"""
    
    id = String(required=True)                             # Restricted
    type_id = Field(Int, default_value=0)                  # Restricted
    params = Field(ElementParams)


class _Dev(ObjectType):
    """Contains collection of elements, accessed by it's id"""
    
    element = Field(Element, el_id=String())
    
    def resolve_element(root, info, el_id, **kwargs):
        el_data = root.get(el_id)
        return Element(**el_data)
    

class NestedStructure(ObjectType):
    """Flowchart settings structure, taken as an example"""
    
    id = String(required=True)                             # Restricted
    name = _ShortString(required=True)
    currency = Field(_Quote, val=String())
    dev = Field(_Dev, el_id=String())
    elements = List(Element)
    
    def resolve_elements(root, info, **kwargs):
        return [Element(**el_data) for el, el_data in root.dev.items()]
