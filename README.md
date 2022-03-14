# graphene-nesting-dict
Graphene utilization to update nested dictionary, allow to update nested data during GraphQL query. The position of updated fields is defined by query. 

A special middleware `StructureUpdate` is designed to intercept field `args`, validate them and update corresponding item in DATA dict. 
If validation of input value has failed - update will be skipped, and your data remains.
Your graphene object should be designed to define data structure and field types.
As a `Scalar` type is an endpoint of field resolving, `StructureUpdate` utilized
`serialize` method of corresponding field to validate input value. 

See and run example.py
