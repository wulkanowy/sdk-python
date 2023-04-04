from datetime import datetime
from enum import Enum
from uuid import UUID
from pydantic import BaseModel, Field, root_validator

from sdk_python.hebe.api import API, FilterListType
from sdk_python.hebe.data.pupil import Pupil
from sdk_python.hebe.error import InvalidResponseEnvelopeTypeException
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
    async def get_by_pupil(api: API, pupil: Pupil, **kwargs) -> list["Exam"]:
        envelope, envelope_type = await api.get(
            entity="exam",
            filter_list_type=FilterListType.BY_PUPIL,
            rest_url=pupil.unit.rest_url,
            pupil_id=pupil.id,
            **kwargs
        )
        if envelope_type != "IEnumerable`1":
            raise InvalidResponseEnvelopeTypeException()
        return [Exam.parse_obj(exam) for exam in envelope]

    @staticmethod
    async def get_by_id(api: API, pupil: Pupil, id: int, **kwargs) -> "Exam":
        envelope, envelope_type = await api.get(
            entity="exam",
            filter_list_type=FilterListType.BY_ID,
            rest_url=pupil.unit.rest_url,
            pupil_id=pupil.id,
            id=id,
            **kwargs
        )
        if envelope_type != "ExamPayload":
            raise InvalidResponseEnvelopeTypeException()
        return Exam.parse_obj(envelope)
