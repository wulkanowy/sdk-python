from uuid import UUID
from pydantic import BaseModel, Field, root_validator
from datetime import datetime
from typing import Optional
from enum import Enum

from sdk_python.hebe.api import API, FilterListType
from sdk_python.hebe.data.pupil import Pupil
from sdk_python.hebe.error import InvalidResponseEnvelopeTypeException
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
    async def get_by_pupil(api: API, pupil: Pupil, **kwargs) -> list["Note"]:
        envelope, envelope_type = await api.get(
            entity="note",
            rest_url=pupil.unit.rest_url,
            filter_list_type=FilterListType.BY_PUPIL,
            pupil_id=pupil.id,
            **kwargs
        )
        if envelope_type != "IEnumerable`1":
            raise InvalidResponseEnvelopeTypeException()
        return [Note.parse_obj(note) for note in envelope]

    @staticmethod
    async def get_by_id(api: API, pupil: Pupil, id: int, **kwargs) -> "Note":
        envelope, envelope_type = await api.get(
            entity="note",
            rest_url=pupil.unit.rest_url,
            filter_list_type=FilterListType.BY_ID,
            pupil_id=pupil.id,
            id=id,
            **kwargs
        )
        if envelope_type != "NotePayload":
            raise InvalidResponseEnvelopeTypeException()
        return Note.parse_obj(envelope)
