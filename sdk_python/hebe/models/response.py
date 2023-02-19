from pydantic import BaseModel, Field
from typing import Any, Union


class ResponseStatus(BaseModel):
    code: int = Field(alias="Code")
    message: str = Field(alias="Message")

    class Config:
        allow_population_by_field_name = True


class Response(BaseModel):
    envelope_type: str = Field(alias="EnvelopeType")
    envelope: Any = Field(alias="Envelope")
    status: ResponseStatus = Field(alias="Status")
    request_id: str = Field(alias="RequestId")
    timestamp: Union[float, int] = Field(alias="Timestamp")
    timestamp_formatted: str = Field(alias="TimestampFormatted")

    class Config:
        allow_population_by_field_name = True
