from datetime import time
from pydantic import BaseModel, Field, root_validator

from sdk_python.hebe.api import API
from sdk_python.hebe.data.pupil import Pupil
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
    async def get(api: API, pupil: Pupil, **kwargs) -> list["TimeSlot"]:
        envelope, envelope_type = await api.get(
            entity="dictionary/timeslot",
            rest_url=pupil.unit.rest_url,
            **kwargs
        )
        if envelope_type != "IEnumerable`1":
            raise InvalidResponseEnvelopeTypeException()
        return [TimeSlot.parse_obj(time_slot) for time_slot in envelope]
