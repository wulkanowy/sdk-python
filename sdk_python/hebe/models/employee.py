from pydantic import BaseModel, Field


class Employee(BaseModel):
    id: int = Field(alias="Id")
    name: str = Field(alias="Name")
    last_name: str = Field(alias="Surname")
    full_name: str = Field(alias="DisplayName")
