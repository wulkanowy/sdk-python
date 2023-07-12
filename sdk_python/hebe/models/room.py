from pydantic import BaseModel, Field


class Room(BaseModel):
    id: int = Field(alias="Id")
    code: str = Field(alias="Code")
