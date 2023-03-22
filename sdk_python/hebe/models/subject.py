from uuid import UUID
from pydantic import BaseModel, Field, root_validator


class Subject(BaseModel):
    id: int = Field(alias="Id")
    key: UUID = Field(alias="Key")
    position: int = Field(alias="Position")
    code: str = Field(alias="Kod")
    name: str = Field(alias="Name")
