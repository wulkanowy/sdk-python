from uuid import UUID
from pydantic import BaseModel, Field


class Team(BaseModel):
    id: int = Field(alias="Id")
    key: UUID = Field(alias="Key")
    symbol: str = Field(alias="Symbol")
    full_name: str = Field(alias="DisplayName")
