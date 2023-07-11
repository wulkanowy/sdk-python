from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, root_validator

from sdk_python.hebe import API
from sdk_python.hebe.error import InvalidResponseEnvelopeTypeException
from sdk_python.hebe.models.employee import Employee
from sdk_python.hebe.models.attachment import Attachment
from sdk_python.hebe.models.subject import Subject


class Homework(BaseModel):
    id: int = Field(alias="Id")
    key: UUID = Field(alias="Key")
    homework_id: int = Field(alias="IdHomework")
    deadline: datetime = Field(alias="Deadline")
    subject: Subject = Field(alias="Subject")
    content: str = Field(alias="Content")
    attachments: list[Attachment] = Field(alias="Attachments")
    date_created: datetime = Field(alias="DateCreated")
    creator: Employee = Field(alias="Creator")
    date_: date = Field(alias="Date")
    answer_required: bool = Field(alias="IsAnswerRequired")
    answer_date: Optional[datetime] = Field(alias="AnswerDate")
    pupil_id: int = Field(alias="IdPupil")

    @root_validator(pre=True)
    def root_validator(cls, values):
        values["Deadline"] = datetime.fromtimestamp(
            values["Deadline"]["Timestamp"] / 1000
        )
        values["DateCreated"] = datetime.fromtimestamp(
            values["DateCreated"]["Timestamp"] / 1000
        )
        values["Date"] = date.fromtimestamp(values["Date"]["Timestamp"] / 1000)
        values["AnswerDate"] = (
            datetime.fromtimestamp(values["AnswerDate"]["Timestamp"] / 1000)
            if values["AnswerDate"]
            else None
        )
        return values

    @staticmethod
    async def get_by_pupil(
        api: API, pupil_id: int, last_sync_date: datetime = datetime.min
    ) -> list["Homework"]:
        envelope = await api.get_all(
            "homework/byPupil",
            {"pupilId": pupil_id, "lastSyncDate": last_sync_date.isoformat()},
        )
        return list(map(Homework.parse_obj, envelope))

    @staticmethod
    async def get_deleted_by_pupil(
        api: API, pupil_id: int, last_sync_date: datetime = datetime.min
    ) -> list[int]:
        envelope, envelope_type = await api.get(
            "homework/deleted/byPupil",
            params={"pupilId": pupil_id, "lastSyncDate": last_sync_date.isoformat()},
        )
        if envelope_type != "IEnumerable`1":
            raise InvalidResponseEnvelopeTypeException()
        return envelope

    @staticmethod
    async def get_deleted(
        api: API, last_sync_date: datetime = datetime.min
    ) -> list[int]:
        envelope, envelope_type = await api.get(
            "homework/deleted",
            params={"lastSyncDate": last_sync_date.isoformat()},
        )
        if envelope_type != "IEnumerable`1":
            raise InvalidResponseEnvelopeTypeException()
        return envelope
