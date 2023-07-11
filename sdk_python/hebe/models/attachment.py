from pydantic import Field, BaseModel


class Attachment(BaseModel):
    name: str = Field(alias="Name")
    link: str = Field(alias="Link")
