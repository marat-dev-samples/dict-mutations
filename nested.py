import graphene
from graphene_chain_mutation import ShareResult
#from .types import ParentType, ParentInput, ChildType, ChildInput

from data import *

class CreateParent(ShareResult, graphene.Mutation, ParentType):
    class Arguments:
        data = ParentInput()
 
    @staticmethod
    def mutate(_: None, __: graphene.ResolveInfo,
               data: ParentInput = None) -> 'CreateParent':
        return CreateParent(**data.__dict__)
 

class CreateChild(ShareResult, graphene.Mutation, ChildType):
    class Arguments:
        data = ChildInput()
 
    @staticmethod
    def mutate(_: None, __: graphene.ResolveInfo,
               data: ChildInput = None) -> 'CreateChild':
        return CreateChild(**data.__dict__)






class Query(graphene.ObjectType):
    parent = graphene.Field(ParentType, pk=graphene.Int())
    parents = graphene.List(ParentType)
    child = graphene.Field(ChildType, pk=graphene.Int())
    children = graphene.List(ChildType)


class Mutation(graphene.ObjectType):
    create_parent = CreateParent.Field()
    create_child = CreateChild.Field()
    set_parent = SetParent.Field()
    add_sibling = AddSibling.Field()


class NullContext: pass


GRAPHQL_NESTING_MUTATION = """
mutation ($parent: ParentInput, $child1: ChildInput, $child2: ChildInput) {
    n1: upsertParent(data: $parent) {
        pk
        name
    }
    
    n2: createChild(data: $child1) {
        pk
        name
        parent: refParent(ref: "n1") {
          pk
          name
        }
    }
    
    n3: createChild(data: $child2) {
        pk
        name
        parent: refParent(ref: "n1") {
          pk
          name
        }
    }
}
"""

VARIABLES = dict(
    parent = dict(
        name = "Emilie"
    )
    ,child1 = dict(
        name = "John"
    )
    ,child2 = dict(
        name = "Julie"
    )
)


schema = graphene.Schema(query=Query, mutation=Mutation)

result = schema.execute(GRAPHQL_MUTATION ,variables = VARIABLES ,context=NullContext())
# If no errors in result - update schema data

print('-'*10)
print(result.data)
print(result.errors)


#query = 'mutation myFirstMutation {addElement(name:"s_in2"){element {id displayName typeId}}}'
#result = schema.execute(query, root=Data)


#print(Data)