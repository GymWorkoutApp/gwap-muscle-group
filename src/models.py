from uuid import uuid4

from gwap_framework.models.base import BaseModel
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID


class MuscleGroupModel(BaseModel):
    __tablename__ = 'muscle_groups'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(100), nullable=False)
