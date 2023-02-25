from pydantic import BaseModel, Field, root_validator
from datetime import datetime

from sdk_python.hebe.data.pupil import Pupil
from sdk_python.hebe.api import API
from sdk_python.hebe.error import InvalidResponseEnvelopeTypeException


class LuckyNumber(BaseModel):
    number: int = Field(alias="Number")
    day: datetime = Field(alias="Day")

    @root_validator(pre=True)
    def root_validator(cls, values):
        values["Day"] = datetime.fromisoformat(values["Day"])
        return values

    @staticmethod
    async def get(api: API, pupil: Pupil, day: datetime) -> "LuckyNumber":
        envelope, envelope_type = await api.request(
            "GET",
            f"{pupil.unit.rest_url}/mobile/school/lucky",
            params={
                "constituentId": pupil.constituent_unit.id,
                "day": day.strftime("%Y-%m-%d"),
            },
        )
        if envelope_type != "LuckyNumberPayload":
            raise InvalidResponseEnvelopeTypeException()
        return LuckyNumber.parse_obj(envelope)
