from uuid import UUID
from pydantic import BaseModel, Field, root_validator


class Subject(BaseModel):
    id: int = Field(alias="Id")
    key: UUID = Field(alias="Key")
    position: int = Field(alias="Position")
    code: str = Field(alias="Kod")
    name: str = Field(alias="Name")

    @root_validator(pre=True)
    def root_validator(cls, values):
        values["Key"] = UUID(values["Key"])
