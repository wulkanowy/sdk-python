from pydantic import BaseModel, Field, root_validator
from datetime import date

from sdk_python.hebe.data.pupil import Pupil
from sdk_python.hebe.api import API
from sdk_python.hebe.error import InvalidResponseEnvelopeTypeException


class LuckyNumber(BaseModel):
    number: int = Field(alias="Number")
    day: date = Field(alias="Day")

    @root_validator(pre=True)
    def root_validator(cls, values):
        values["Day"] = date.fromisoformat(values["Day"])
        return values

    @staticmethod
    async def get(
        api: API, pupil: Pupil, day: date = date.today(), **kwargs
    ) -> "LuckyNumber":
        envelope, envelope_type = await api.get(
            entity="school/lucky",
            rest_url=pupil.unit.rest_url,
            day=day,
            constituent_unit_id=pupil.constituent_unit.id,
            **kwargs
        )
        if envelope_type != "LuckyNumberPayload":
            raise InvalidResponseEnvelopeTypeException()
        return LuckyNumber.parse_obj(envelope)
