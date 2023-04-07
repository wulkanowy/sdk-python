from uuid import UUID
from pydantic import BaseModel, Field


class Distribution(BaseModel):
    id: int = Field(alias="Id")
    key: UUID = Field(alias="Key")
    short: str = Field(alias="Shortcut")
    name: str = Field(alias="Name")
    part_type: str = Field(alias="PartType")
