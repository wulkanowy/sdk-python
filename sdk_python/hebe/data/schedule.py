from datetime import date, datetime
from enum import Enum
from typing import Optional, Any

from pydantic import BaseModel, Field, root_validator

from sdk_python.hebe import API
from sdk_python.hebe.data.time_slot import TimeSlot
from sdk_python.hebe.error import InvalidResponseEnvelopeTypeException
from sdk_python.hebe.models.distribution import Distribution
from sdk_python.hebe.models.employee import Employee
from sdk_python.hebe.models.room import Room
from sdk_python.hebe.models.subject import Subject
from sdk_python.hebe.models.team import Team


class ScheduleChangeType(Enum):
    EXEMPTION = 1
    SUBSTITUTION = 2
    RESCHEDULED = 3
    CLASS_ABSENCE = 4


class ScheduleEntryChange(BaseModel):
    id: int = Field(alias="Id")
    type: ScheduleChangeType = Field(alias="Type")
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
    team: Optional[Team] = Field(alias="Clazz")
    distribution: Optional[Distribution] = Field(alias="Distribution")
    event: Optional[str] = Field(alias="Event")
    pupil_alias: Optional[str] = Field(alias="PupilAlias")
    change: Optional[ScheduleEntryChange] = Field(alias="Change")
    merge_change_id: Optional[int] = Field(alias="MergeChangeId")
    visible: bool = Field(alias="Visible")

    @root_validator(pre=True)
    def root_validator(cls, values):
        values["Date"] = date.fromtimestamp(values["Date"]["Timestamp"] / 1000)
        return values

    @staticmethod
    async def get_by_pupil(
        api: API,
        pupil_id: int,
        date_from: date.today(),
        date_to: date = date.today(),
        last_sync_date: datetime = datetime.min,
    ) -> list["ScheduleEntry"]:
        envelope = await api.get_all(
            "schedule/byPupil",
            {
                "pupilId": pupil_id,
                "dateFrom": date_from.isoformat(),
                "dateTo": date_to.isoformat(),
                "lastSyncDate": last_sync_date.isoformat(),
            },
        )
        return list(map(ScheduleEntry.parse_obj, envelope))

    @staticmethod
    async def get_deleted_by_pupil(
        api: API, pupil_id: int, last_sync_date: datetime = datetime.min
    ) -> list[int]:
        envelope, envelope_type = await api.get(
            "schedule/deleted/byPupil",
            params={"pupilId": pupil_id, "lastSyncDate": last_sync_date.isoformat()},
        )
        if envelope_type != "IEnumerable`1":
            raise InvalidResponseEnvelopeTypeException()
        return envelope


class ScheduleChange(BaseModel):
    id: int = Field(alias="Id")
    schedule_entry_id: int = Field(alias="ScheduleId")
    type: ScheduleChangeType = Field(alias="Type")
    merge: bool = Field(alias="IsMerge")
    separation: bool = Field(alias="Separation")
    lesson_date: date = Field(alias="LessonDate")
    change_date: Optional[date] = Field(alias="ChangeDate")
    time_slot: Optional[TimeSlot] = Field(alias="TimeSlot")
    subject: Optional[Subject] = Field(alias="Subject")
    teacher_primary: Optional[Employee] = Field(alias="TeacherPrimary")
    teacher_secondary: Optional[Employee] = Field(alias="TeacherSecondary")
    room: Optional[Room] = Field(alias="Room")
    team: Optional[Team] = Field(alias="Clazz")
    distribution: Optional[Distribution] = Field(alias="Distribution")
    event: Optional[Any] = Field(alias="Event")
    note: Optional[str] = Field(alias="Note")
    reason: Optional[str] = Field(alias="Reason")
    unit_id: int = Field(alias="UnitId")

    @root_validator(pre=True)
    def root_validator(cls, values):
        values["Type"] = values["Change"]["Type"]
        values["IsMerge"] = values["Change"]["IsMerge"]
        values["Separation"] = values["Change"]["Separation"]
        values["LessonDate"] = datetime.fromtimestamp(
            values["LessonDate"]["Timestamp"] / 1000
        )
        values["ChangeDate"] = (
            datetime.fromtimestamp(values["ChangeDate"]["Timestamp"] / 1000)
            if values["ChangeDate"]
            else None
        )
        return values

    @staticmethod
    async def get_by_pupil(
        api: API,
        pupil_id: int,
        date_from: date = date.today(),
        date_to: date = date.today(),
        last_sync_date: datetime = datetime.min,
    ) -> list["ScheduleChange"]:
        envelope = await api.get_all(
            "schedule/changes/byPupil",
            {
                "pupilId": pupil_id,
                "dateFrom": date_from.isoformat(),
                "dateTo": date_to.isoformat(),
                "lastSyncDate": last_sync_date.isoformat(),
            },
        )
        return list(map(ScheduleChange.parse_obj, envelope))

    @staticmethod
    async def get_deleted(
        api: API, last_sync_date: datetime = datetime.min
    ) -> list[int]:
        envelope, envelope_type = await api.get(
            "schedule/changes/deleted",
            params={"lastSyncDate": last_sync_date.isoformat()},
        )
        if envelope_type != "IEnumerable`1":
            raise InvalidResponseEnvelopeTypeException()
        return envelope
