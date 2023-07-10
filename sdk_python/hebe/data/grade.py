from pydantic import BaseModel, Field, root_validator
from datetime import datetime
from typing import Optional
from enum import Enum
from uuid import UUID

from sdk_python.hebe.api import API
from sdk_python.hebe.error import (
    InvalidResponseEnvelopeTypeException,
    NotFoundEntityException,
)
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
    async def get_by_pupil_and_period(
        api: API,
        pupil_id: int,
        period_id: int,
        behaviour: bool = False,
        last_sync_date: datetime = datetime.min,
    ) -> list["Grade"]:
        envelope = await api.get_all(
            f'grade/{"behaviour" if behaviour else ""}/byPupil',
            {
                "pupilId": pupil_id,
                "periodId": period_id,
                "lastSyncDate": last_sync_date.isoformat(),
            },
        )
        return list(map(Grade.parse_obj, envelope))

    @staticmethod
    async def get_by_pupil_period_and_id(
        api: API, pupil_id: int, period_id: int, grade_id: int
    ) -> "Grade":
        envelope, envelope_type = await api.get(
            "grade/ById",
            params={"pupilId": pupil_id, "periodId": period_id, "id": grade_id},
        )
        if envelope_type != "GradePayload":
            raise InvalidResponseEnvelopeTypeException()
        if not envelope:
            raise NotFoundEntityException()
        return Grade.parse_obj(envelope)

    @staticmethod
    async def get_deleted_by_pupil_and_period(
        api: API, pupil_id: int, period_id: int, last_sync_date: datetime = datetime.min
    ) -> list[int]:
        envelope, envelope_type = await api.get(
            "grade/deleted/byPupil",
            params={
                "pupilId": pupil_id,
                "periodId": period_id,
                "lastSyncDate": last_sync_date.isoformat(),
            },
        )
        if envelope_type != "IEnumerable`1":
            raise InvalidResponseEnvelopeTypeException()
        return envelope

    @staticmethod
    async def get_deleted(
        api: API, last_sync_date: datetime = datetime.min
    ) -> list[int]:
        envelope, envelope_type = await api.get(
            "grade/deleted",
            params={"lastSyncDate": last_sync_date.isoformat()},
        )
        if envelope_type != "IEnumerable`1":
            raise InvalidResponseEnvelopeTypeException()
        return envelope


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
    async def get_by_pupil_and_period(
        api: API, pupil_id: int, period_id: int, last_sync_date: datetime = datetime.min
    ) -> list["GradesSummary"]:
        envelope = await api.get_all(
            "grade/summary/byPupil",
            {
                "pupilId": pupil_id,
                "periodId": period_id,
                "lastSyncDate": last_sync_date.isoformat(),
            },
        )
        return list(map(GradesSummary.parse_obj, envelope))
