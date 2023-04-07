from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel, Field, root_validator
from datetime import date

from sdk_python.hebe.api import API, FilterListType
from sdk_python.hebe.data.pupil import Pupil
from sdk_python.hebe.data.time_slot import TimeSlot
from sdk_python.hebe.error import InvalidResponseEnvelopeTypeException
from sdk_python.hebe.models.distribution import Distribution
from sdk_python.hebe.models.employee import Employee
from sdk_python.hebe.models.room import Room
from sdk_python.hebe.models.subject import Subject
from sdk_python.hebe.models.team import Team


class ScheludeEntryChangeType(Enum):
    EXEMPTION = 1
    SUBSTITUTION = 2
    RESCHELUDED = 3
    CLASS_ABSENCE = 4


class ScheludeEntryChange(BaseModel):
    id: int = Field(alias="Id")
    type: ScheludeEntryChangeType = Field(alias="Type")
    merge: bool = Field(alias="IsMerge")
    separation: bool = Field(alias="Separation")


class ScheduleEntry(BaseModel):
    id: int = Field(alias="Id")
    date_: date = Field(alias="Date")
    time_slot: TimeSlot = Field(alias="TimeSlot")
    subject: Optional[Subject] = Field(alias="Subject")
    teacher_primary: Optional[Employee] = Field(alias="TeacherPrimary")
    teacher_secondary: Optional[Employee] = Field(alias="TeacherSecondary")
    room: Optional[Room] = Field(alias="Room")
    team: Optional[Team] = Field(alias="Team")
    distribution: Optional[Distribution] = Field(alias="Distribution")
    event: Optional[Any] = Field(alias="Event")
    pupil_alias: Optional[str] = Field(alias="PupilAlias")
    change: Optional[ScheludeEntryChange] = Field(alias="Change")
    merge_change_id: Optional[int] = Field(alias="MergeChangeId")
    visible: bool = Field(alias="Visible")

    @root_validator(pre=True)
    def root_validator(cls, values):
        values["Date"] = date.fromtimestamp(values["Date"]["Timestamp"] / 1000)
        return values

    @staticmethod
    async def get_by_pupil(
        api: API, pupil: Pupil, date_from: date, date_to: date, **kwargs
    ) -> list["ScheduleEntry"]:
        envelope, envelope_type = await api.get(
            entity="schedule",
            rest_url=pupil.unit.rest_url,
            filter_list_type=FilterListType.BY_PUPIL,
            pupil_id=pupil.id,
            date_from=date_from,
            date_to=date_to,
            **kwargs
        )
        if envelope_type != "IEnumerable`1":
            raise InvalidResponseEnvelopeTypeException()
        return [ScheduleEntry.parse_obj(schedule_entry) for schedule_entry in envelope]
