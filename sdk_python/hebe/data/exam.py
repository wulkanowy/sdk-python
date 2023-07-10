from datetime import datetime
from enum import Enum
from uuid import UUID
from pydantic import BaseModel, Field, root_validator

from sdk_python.hebe.api import API
from sdk_python.hebe.error import (
    InvalidResponseEnvelopeTypeException,
    NotFoundEntityException,
)
from sdk_python.hebe.models.employee import Employee
from sdk_python.hebe.models.subject import Subject


class ExamType(Enum):
    PAPER = "Kartkówka"
    TEST = "Sprawdzian"
    CLASS_WORK = "Praca klasowa"


class Exam(BaseModel):
    id: int = Field(alias="Id")
    key: UUID = Field(alias="Key")
    type: ExamType = Field(alias="Type")
    deadline: datetime = Field(alias="Deadline")
    subject: Subject = Field(alias="Subject")
    content: str = Field(alias="Content")
    date_created: datetime = Field(alias="DateCreated")
    creator: Employee = Field(alias="Creator")
    date_modify: datetime = Field(alias="DateModify")
    pupil_id: int = Field(alias="PupilId")

    @root_validator(pre=True)
    def root_validator(cls, values):
        values["Deadline"] = datetime.fromtimestamp(
            values["Deadline"]["Timestamp"] / 1000
        )
        values["DateCreated"] = datetime.fromtimestamp(
            values["DateCreated"]["Timestamp"] / 1000
        )
        values["DateModify"] = datetime.fromtimestamp(
            values["DateModify"]["Timestamp"] / 1000
        )
        return values

    @staticmethod
    async def get_by_pupil(
        api: API, pupil_id: int, last_sync_date: datetime = datetime.min
    ) -> list["Exam"]:
        envelope = await api.get_all(
            "exam/byPupil",
            {"pupilId": pupil_id, "lastSyncDate": last_sync_date.isoformat()},
        )
        return list(map(Exam.parse_obj, envelope))

    @staticmethod
    async def get_by_pupil_and_id(api: API, pupil_id: int, exam_id: int) -> "Exam":
        envelope, envelope_type = await api.get(
            "exam/byId", params={"pupilId": pupil_id, "id": exam_id}
        )
        if envelope_type != "ExamPayload":
            raise InvalidResponseEnvelopeTypeException()
        if not envelope:
            raise NotFoundEntityException()
        return Exam.parse_obj(envelope)

    @staticmethod
    async def get_deleted(
        api: API, last_sync_date: datetime = datetime.min
    ) -> list[int]:
        envelope, envelope_type = await api.get(
            "exam/deleted", params={"lastSyncDate": last_sync_date.isoformat()}
        )
        if envelope_type != "IEnumerable`1":
            raise InvalidResponseEnvelopeTypeException()
        return envelope

    @staticmethod
    async def get_deleted_by_pupil(
        api: API, pupil_id: int, last_sync_date: datetime = datetime.min
    ) -> list[int]:
        envelope, envelope_type = await api.get(
            "exam/deleted/byPupil",
            params={"pupilId": pupil_id, "lastSyncDate": last_sync_date.isoformat()},
        )
        if envelope_type != "IEnumerable`1":
            raise InvalidResponseEnvelopeTypeException()
        return envelope
