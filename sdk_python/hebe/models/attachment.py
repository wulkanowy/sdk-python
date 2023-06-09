from pydantic import BaseModel, Field


class Attachment(BaseModel):
    name: str = Field(alias="Name")
    link: str = Field(alias="Link")
