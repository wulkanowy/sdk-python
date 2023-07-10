from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, root_validator

from sdk_python.hebe.api import API
from sdk_python.hebe.error import (
    InvalidResponseEnvelopeTypeException,
    NotFoundEntityException,
)


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
        api: API,
        pupil_id: int,
        from_date: date = datetime.now(),
        last_sync_date: datetime = datetime.min,
    ) -> list["Meeting"]:
        envelope = await api.get_all(
            "meetings/byPupil",
            {
                "pupilId": pupil_id,
                "from": from_date.isoformat(),
                "lastSyncDate": last_sync_date.isoformat(),
            },
        )
        return list(map(Meeting.parse_obj, envelope))

    @staticmethod
    async def get_by_pupil_and_id(
        api: API, pupil_id: int, meeting_id: int
    ) -> "Meeting":
        envelope, envelope_type = await api.get(
            "meetings/byId", params={"pupilId": pupil_id, "id": meeting_id}
        )
        if envelope_type != "MeetingPayload":
            raise InvalidResponseEnvelopeTypeException()
        if not envelope:
            raise NotFoundEntityException()
        return Meeting.parse_obj(envelope)

    @staticmethod
    async def get_deleted_by_pupil(
        api: API, pupil_id: int, last_sync_date: datetime = datetime.min
    ) -> list[int]:
        envelope, envelope_type = await api.get(
            "meetings/deleted/byPupil",
            params={"pupilId": pupil_id, "lastSyncDate": last_sync_date.isoformat()},
        )
        if envelope_type != "IEnumerable`1":
            raise InvalidResponseEnvelopeTypeException()
        return envelope
