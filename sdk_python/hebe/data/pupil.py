from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, root_validator
from enum import Enum

from sdk_python.hebe.api import API
from sdk_python.hebe.error import InvalidResponseEnvelopeTypeException


class LoginRole(Enum):
    PUPIL = "Uczen"
    GUARDIAN = "Opiekun"


class Sex(Enum):
    MAN = True
    WOMAN = False


class Capability(Enum):
    REGULAR = "REGULAR"
    REALIZED_LESSONS = "LESSONS_VISIBLE"
    PLANNED_LESSONS = "PLANNED_VISIBLE"
    GRADES_AVG = "AVG_ENABLED"
    JUSTIFICATIONS = "JUSTIFICATIONS_ENABLED"
    POINTS = "POINTS_ENABLED"
    EATERY = "EATERY"


class Login(BaseModel):
    id: int = Field(alias="Id")
    value: str = Field(alias="Value")
    role: LoginRole = Field(alias="LoginRole")
    first_name: str = Field(alias="FirstName")
    second_name: str = Field(alias="SecondName")
    last_name: str = Field(alias="Surname")
    full_name: str = Field(alias="DisplayName")


class Unit(BaseModel):
    id: int = Field(alias="Id")
    short: str = Field(alias="Short")
    symbol: str = Field(alias="Symbol")
    name: str = Field(alias="Name")
    full_name: str = Field(alias="DisplayName")
    patron: Optional[str] = Field(alias="Patron")
    address: str = Field(alias="Address")
    rest_url: str = Field(alias="RestURL")
    school_topic: str = Field(alias="SchoolTopic")


class ConstituentUnit(BaseModel):
    id: int = Field(alias="Id")
    short: str = Field(alias="Short")
    name: str = Field(alias="Name")
    patron: Optional[str] = Field(alias="Patron")
    address: str = Field(alias="Address")
    school_topic: str = Field(alias="SchoolTopic")


class Pupil(BaseModel):
    id: int = Field(alias="Id")
    login_id: int = Field(alias="LoginId")
    login_value: str = Field(alias="LoginValue")
    first_name: str = Field(alias="FirstName")
    second_name: str = Field(alias="SecondName")
    last_name: str = Field(alias="Surname")
    sex: Sex = Field(alias="Sex")

    @staticmethod
    async def get_by_id(api: API, pupil_id: int) -> "Pupil":
        envelope, envelope_type = await api.get("pupil", params={"id": pupil_id})
        if envelope_type != "PupilPayload":
            raise InvalidResponseEnvelopeTypeException()
        return Pupil.parse_obj(envelope)


class Period(BaseModel):
    id: int = Field(alias="Id")
    number: int = Field(alias="Number")
    level: int = Field(alias="Level")
    start: datetime = Field(alias="Start")
    end: datetime = Field(alias="End")
    current: bool = Field(alias="Current")
    last_in_year: bool = Field(alias="Last")
    capabilities: list[str] = Field(alias="Capabilities")

    @root_validator(pre=True)
    def root_validator(cls, values):
        values["Start"] = datetime.fromtimestamp(values["Start"]["Timestamp"] / 1000)
        values["End"] = datetime.fromtimestamp(values["End"]["Timestamp"] / 1000)
        return values


class Journal(BaseModel):
    id: int = Field(alias="Id")
    year_start: datetime = Field(alias="YearStart")
    year_end: datetime = Field(alias="YearEnd")
    pupil_number: int = Field(alias="PupilNumber")

    @root_validator(pre=True)
    def root_validator(cls, values):
        values["YearStart"] = datetime.fromtimestamp(
            values["YearStart"]["Timestamp"] / 1000
        )
        values["YearEnd"] = datetime.fromtimestamp(
            values["YearEnd"]["Timestamp"] / 1000
        )
        return values


class MessageBox(BaseModel):
    id: int = Field(alias="Id")
    name: str = Field(alias="Name")
    global_key: str = Field(alias="GlobalKey")


class PupilInfo(BaseModel):
    top_level_partition: str = Field(alias="TopLevelPartition")
    partition: str = Field(alias="Partition")
    team_name: str = Field(alias="ClassDisplay")
    login: Login = Field(alias="Login")
    unit: Unit = Field(alias="Unit")
    constituent_unit: ConstituentUnit = Field(alias="ConstituentUnit")
    capabilities: list[Capability] = Field(alias="Capabilities")
    pupil: Pupil = Field(alias="Pupil")
    periods: list[Period] = Field(alias="Periods")
    current_journal: Journal = Field(alias="Journal")
    context: str = Field(alias="Context")
    message_box: MessageBox = Field(alias="MessageBox")

    @staticmethod
    async def get(
        api: API, last_sync_date: datetime = datetime.min
    ) -> list["PupilInfo"]:
        envelope, envelope_type = await api.get(
            "register/hebe",
            params={"lastSyncDate": last_sync_date.isoformat(), "mode": 2},
        )
        if envelope_type != "IEnumerable`1":
            raise InvalidResponseEnvelopeTypeException()
        return list(map(PupilInfo.parse_obj, envelope))
