from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, root_validator

from sdk_python.hebe.api import API, FilterListType
from sdk_python.hebe.data.pupil import Period, Pupil
from sdk_python.hebe.error import InvalidResponseEnvelopeTypeException


class Meeting(BaseModel):
    id: int = Field(alias="Id")
    subject: str = Field(alias="Why")
    date: datetime = Field(alias="When")
    place: str = Field(alias="Where")
    agenda: str = Field(alias="Agenda")
    online: Optional[str] = Field(alias="Online")
    additional_info: Optional[str] = Field(alias="AdditionalInfo")

    @root_validator(pre=True)
    def root_validator(cls, values):
        values["When"] = datetime.fromtimestamp(values["When"]["Timestamp"] / 1000)
        return values

    @staticmethod
    async def get_by_pupil(
        api: API, pupil: Pupil, from_: date = None, **kwargs
    ) -> list["Meeting"]:
        envelope, envelope_type = await api.get(
            entity="meetings",
            filter_list_type=FilterListType.BY_PUPIL,
            rest_url=pupil.unit.rest_url,
            pupil_id=pupil.id,
            from_=from_ if from_ else pupil.periods[0].start.date(),
            **kwargs
        )
        if envelope_type != "IEnumerable`1":
            raise InvalidResponseEnvelopeTypeException()
        return [Meeting.parse_obj(meeting) for meeting in envelope]

    @staticmethod
    async def get_by_id(
        api: API, pupil: Pupil, id: int, **kwargs
    ) -> "Meeting":
        envelope, envelope_type = await api.get(
            entity="meetings",
            filter_list_type=FilterListType.BY_ID,
            rest_url=pupil.unit.rest_url,
            pupil_id=pupil.id,
            id=id,
            **kwargs
        )
        if envelope_type != "MeetingPayload":
            raise InvalidResponseEnvelopeTypeException()
        return Meeting.parse_obj(envelope)
