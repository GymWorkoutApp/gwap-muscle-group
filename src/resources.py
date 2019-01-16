from typing import Dict
from uuid import uuid4

from gwap_framework.resource.base import BaseResource
from gwap_framework.utils.decorators import validate_schema

from src.cache import cache
from src.database import master_async_session, read_replica_async_session
from src.models import MuscleGroupModel
from src.schemas import MuscleGroupInputSchema, MuscleGroupOutputSchema


class MuscleGroupResource(BaseResource):
    cache = cache
    method_decorators = {
        'create': [validate_schema(MuscleGroupInputSchema)],
        'update': [validate_schema(MuscleGroupInputSchema)],
    }

    def create(self, request_model: 'MuscleGroupInputSchema') -> Dict:
        muscle_group = MuscleGroupModel()
        muscle_group.id = request_model.muscle_group_id or str(uuid4())
        muscle_group.name = request_model.name

        with master_async_session() as session:
            session.add(muscle_group)
            output = MuscleGroupOutputSchema()
            output.muscle_group_id = muscle_group.id
            output.name = muscle_group.name

            output.validate()
            return output.to_primitive()

    def update(self, request_model: 'MuscleGroupInputSchema', muscle_group_id=None):
        muscle_group = MuscleGroupModel()
        muscle_group.id = muscle_group_id
        muscle_group.name = request_model.name

        with master_async_session() as session:
            session.merge(muscle_group)
            output = MuscleGroupOutputSchema()
            output.muscle_group_id = muscle_group.id
            output.name = muscle_group.name

            output.validate()
            return output.to_primitive()

    def list(self, args=None, kwargs=None):
        with read_replica_async_session() as session:
            results = []
            for muscle_group in session.query(MuscleGroupModel).all():
                output = MuscleGroupOutputSchema()
                output.muscle_group_id = muscle_group.id
                output.name = muscle_group.name

                output.validate()
                results.append(output.to_primitive())
        return results

    def retrieve(self, muscle_group_id):
        with read_replica_async_session() as session:
            muscle_group = session.query(MuscleGroupModel).filter_by(id=muscle_group_id).first()
            output = MuscleGroupOutputSchema()
            output.id = muscle_group.id
            output.name = muscle_group.name

            output.validate()
            return output.to_primitive()

    def destroy(self, muscle_group_id):
        with master_async_session() as session:
            session.query(MuscleGroupModel).filter_by(id=muscle_group_id).delete()
            return None


resources_v1 = [
    {'resource': MuscleGroupResource, 'urls': ['/muscle-groups/<muscle_group_id>'], 'endpoint': 'MuscleGroups MuscleGroupId',
     'methods': ['GET', 'PUT', 'PATCH', 'DELETE']},
    {'resource': MuscleGroupResource, 'urls': ['/muscle-groups'], 'endpoint': 'MuscleGroups',
     'methods': ['POST', 'GET']},
]
