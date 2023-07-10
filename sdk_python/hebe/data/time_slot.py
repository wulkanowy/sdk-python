from datetime import time
from pydantic import BaseModel, Field, root_validator

from sdk_python.hebe.api import API
from sdk_python.hebe.error import InvalidResponseEnvelopeTypeException


class TimeSlot(BaseModel):
    id: int = Field(alias="Id")
    position: int = Field(alias="Position")
    start: time = Field(alias="Start")
    end: time = Field(alias="End")

    @root_validator(pre=True)
    def root_validator(cls, values):
        values["Start"] = time(*map(int, values["Start"].split(":")))
        values["End"] = time(*map(int, values["End"].split(":")))
        return values

    @staticmethod
    async def get(api: API) -> list["TimeSlot"]:
        envelope, envelope_type = await api.get("dictionary/timeslot")
        if envelope_type != "IEnumerable`1":
            raise InvalidResponseEnvelopeTypeException()
        return list(map(TimeSlot.parse_obj, envelope))
