import json
from uuid import UUID
from pydantic import BaseModel, Field, root_validator
from datetime import datetime
from typing import Optional
from enum import Enum

from sdk_python.hebe.api import API
from sdk_python.hebe.error import (
    InvalidResponseEnvelopeTypeException,
    NotFoundEntityException,
)
from sdk_python.hebe.models.employee import Employee


class NoteCategoryType(Enum):
    NEGATIVE = "negatywna"
    POSITIVE = "pozytywna"


class NoteCategory(BaseModel):
    id: int = Field(alias="Id")
    name: str = Field(alias="Name")
    default_points: Optional[float] = Field(alias="DefaultPoints")
    type: Optional[NoteCategoryType] = Field(alias="Type")


class Note(BaseModel):
    id: int = Field(alias="Id")
    key: UUID = Field(alias="Key")
    points: Optional[float] = Field(alias="Points")
    positive: bool = Field(alias="Positive")
    content: str = Field(alias="Content")
    creator: Employee = Field(alias="Creator")
    category: Optional[NoteCategory] = Field(alias="Category")
    date_valid: datetime = Field(alias="DateValid")
    date_modify: datetime = Field(alias="DateModify")

    @root_validator(pre=True)
    def root_validator(cls, values):
        values["Key"] = UUID(values["Key"])
        values["DateValid"] = datetime.fromtimestamp(
            values["DateValid"]["Timestamp"] / 1000
        )
        values["DateModify"] = datetime.fromtimestamp(
            values["DateModify"]["Timestamp"] / 1000
        )
        return values

    @staticmethod
    async def get_by_pupil(
        api: API, pupil_id: int, last_sync_date: datetime = datetime.min
    ) -> list["Note"]:
        envelope = await api.get_all(
            "note/byPupil",
            params={"pupilId": pupil_id, "lastSyncDate": last_sync_date.isoformat()},
        )
        return list(map(Note.parse_obj, envelope))

    @staticmethod
    async def get_by_pupil_and_id(api: API, pupil_id: int, note_id: int) -> "Note":
        envelope, envelope_type = await api.get(
            "note/byId", params={"pupilId": pupil_id, "id": note_id}
        )
        if envelope_type != "NotePayload":
            raise InvalidResponseEnvelopeTypeException()
        if not envelope:
            raise NotFoundEntityException()
        return Note.parse_obj(envelope)

    @staticmethod
    async def get_deleted_by_pupil(
        api: API, pupil_id: int, last_sync_date: datetime = datetime.min
    ) -> list[int]:
        envelope, envelope_type = await api.get(
            "note/deleted/byPupil",
            params={"pupilId": pupil_id, "lastSyncDate": last_sync_date.isoformat()},
        )
        if envelope_type != "NotePayload":
            raise InvalidResponseEnvelopeTypeException()
        return envelope
