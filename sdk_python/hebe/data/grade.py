from pydantic import BaseModel, Field, root_validator
from datetime import datetime
from typing import Optional
from enum import Enum
from uuid import UUID

from sdk_python.hebe.api import API, FilterListType
from sdk_python.hebe.data.pupil import Period, Pupil
from sdk_python.hebe.error import InvalidResponseEnvelopeTypeException
from sdk_python.hebe.models.employee import Employee
from sdk_python.hebe.models.subject import Subject


class GradeColumnColor(Enum):
    BLACK = 0
    GREEN = 7261447
    PURPLE = 11627761
    RED = 15748172
    BLUE = 2139383


class GradeColumnCategory(BaseModel):
    id: str = Field(alias="Id")
    code: str = Field(alias="Code")
    name: str = Field(alias="Name")


class GradeColumn(BaseModel):
    id: int = Field(alias="Id")
    key: UUID = Field(alias="Key")
    number: int = Field(alias="Number")
    short: Optional[str] = Field(alias="Code")
    group_name: Optional[str] = Field(alias="Group")
    subject: Subject = Field(alias="Subject")
    name: str = Field(alias="Name")
    color: GradeColumnColor = Field(alias="Color")
    weight: Optional[float] = Field(alias="Weight")
    category: Optional[GradeColumnCategory] = Field(alias="Category")
    period_id: int = Field(alias="PeriodId")

    @root_validator(pre=True)
    def root_validator(cls, values):
        values["Key"] = UUID(values["Key"])
        return values


class Grade(BaseModel):
    id: int = Field(alias="Id")
    key: UUID = Field(alias="Key")
    content: str = Field(alias="Content")
    content_raw: str = Field(alias="ContentRaw")
    comment: Optional[str] = Field(alias="Comment")
    value: Optional[float] = Field(alias="Value")
    column: GradeColumn = Field(alias="Column")
    date_created: Optional[datetime] = Field(alias="DateCreated")
    creator: Employee = Field(alias="Creator")
    date_modify: datetime = Field(alias="DateModify")
    modifier: Employee = Field(alias="Modifier")
    nominator: Optional[float] = Field(alias="Nominator")
    denominator: Optional[float] = Field(alias="Denominator")
    pupil_id: int = Field(alias="PupilId")

    @root_validator(pre=True)
    def root_validator(cls, values):
        values["Key"] = UUID(values["Key"])
        values["DateCreated"] = datetime.fromtimestamp(
            values["DateCreated"]["Timestamp"] / 1000
        )
        values["DateModify"] = datetime.fromtimestamp(
            values["DateModify"]["Timestamp"] / 1000
        )
        return values

    @staticmethod
    async def get_by_pupil(
        api: API, pupil: Pupil, period: Period, behaviour: bool = False, **kwargs
    ) -> list["Grade"]:
        envelope, envelope_type = await api.get(
            entity=f'grade{"/behaviour" if behaviour else ""}',
            rest_url=pupil.unit.rest_url,
            filter_list_type=FilterListType.BY_PUPIL,
            pupil_id=pupil.id,
            period_id=period.id,
            **kwargs
        )
        if envelope_type != "IEnumerable`1":
            raise InvalidResponseEnvelopeTypeException()
        return [Grade.parse_obj(grade) for grade in envelope]

    @staticmethod
    async def get_by_id(
        api: API, pupil: Pupil, period: Period, id: int, **kwargs
    ) -> "Grade":
        envelope, envelope_type = await api.get(
            entity="grade",
            rest_url=pupil.unit.rest_url,
            filter_list_type=FilterListType.BY_ID,
            pupil_id=pupil.id,
            period_id=period.id,
            id=id,
            **kwargs
        )
        if envelope_type != "GradePayload":
            raise InvalidResponseEnvelopeTypeException()
        return Grade.parse_obj(envelope)


class GradesSummary(BaseModel):
    id: int = Field(alias="Id")
    subject: Subject = Field(alias="Subject")
    proposed_grade: Optional[str] = Field(alias="Entry_1")
    final_grade: Optional[str] = Field(alias="Entry_2")
    total_points: Optional[str] = Field(alias="Entry_3")
    date_modify: Optional[datetime] = Field(alias="DateModify")
    period_id: int = Field(alias="PeriodId")
    pupil_id: int = Field(alias="PupilId")

    @root_validator(pre=True)
    def root_validator(cls, values):
        try:
            values["DateModify"] = datetime.fromtimestamp(
                values["DateModify"]["Timestamp"] / 1000
            )
        except:
            values["DateModify"] = None
        return values

    @staticmethod
    async def get_by_pupil(
        api: API, pupil: Pupil, period: Period, **kwargs
    ) -> list["GradesSummary"]:
        envelope, envelope_type = await api.get(
            entity="grade/summary",
            rest_url=pupil.unit.rest_url,
            filter_list_type=FilterListType.BY_PUPIL,
            pupil_id=pupil.id,
            period_id=period.id,
            **kwargs
        )
        if envelope_type != "IEnumerable`1":
            raise InvalidResponseEnvelopeTypeException()
        return [GradesSummary.parse_obj(grades_summary) for grades_summary in envelope]
