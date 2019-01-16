from gwap_framework.schemas.base import BaseSchema
from schematics.types import StringType, DateTimeType, BooleanType, ListType, ModelType, NumberType, IntType


class MuscleGroupInputSchema(BaseSchema):
    muscle_group_id = StringType(required=False, serialized_name='muscle_groupId')
    name = StringType(required=True, max_length=100, min_length=1)


class MuscleGroupOutputSchema(BaseSchema):
    muscle_group_id = StringType(required=False, serialized_name='muscle_groupId')
    name = StringType(required=True, max_length=100, min_length=1)
