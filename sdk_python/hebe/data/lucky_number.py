from pydantic import BaseModel, Field, root_validator
from datetime import date

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
    async def get_by_constituent_unit(
        api: API, constituent_unit_id: int, day: date = date.today()
    ) -> "LuckyNumber":
        envelope, envelope_type = await api.get(
            "school/lucky",
            params={"constituentId": constituent_unit_id, "day": day.isoformat()},
        )
        if envelope_type != "LuckyNumberPayload":
            raise InvalidResponseEnvelopeTypeException()
        return LuckyNumber.parse_obj(envelope)
