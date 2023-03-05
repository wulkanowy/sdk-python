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


class Scope(Enum):
    REGULAR = "REGULAR"
    REALIZED_LESSONS = "LESSONS_VISIBLE"
    PLANNED_LESSONS = "PLANNED_VISIBLE"
    GRADES_AVG = "AVG_ENABLED"
    JUSTIFICATIONS = "JUSTIFICATIONS_ENABLED"


class Unit(BaseModel):
    id: int = Field(alias="Id")
    short: str = Field(alias="Short")
    symbol: str = Field(alias="Symbol")
    group: str = Field(alias="Group")
    name: str = Field(alias="Name")
    full_name: str = Field(alias="DisplayName")
    patron: str = Field(alias="Patron")
    address: str = Field(alias="Address")
    rest_url: str = Field(alias="RestURL")
    school_topic: str = Field(alias="SchoolTopic")


class ConstituentUnit(BaseModel):
    id: int = Field(alias="Id")
    short: str = Field(alias="Short")
    name: str = Field(alias="Name")
    patron: str = Field(alias="Patron")
    address: str = Field(alias="Address")
    school_topic: str = Field(alias="SchoolTopic")


class UserLogin(BaseModel):
    id: int = Field(alias="Id")
    value: str = Field(alias="Value")
    role: LoginRole = Field(alias="LoginRole")
    first_name: str = Field(alias="FirstName")
    second_name: str = Field(alias="SecondName")
    last_name: str = Field(alias="Surname")


class Journal(BaseModel):
    id: int = Field(alias="Id")
    start: datetime = Field(alias="YearStart")
    end: datetime = Field(alias="YearEnd")

    @root_validator(pre=True)
    def root_validator(cls, values):
        values["YearStart"] = datetime.fromtimestamp(
            values["YearStart"]["Timestamp"] / 1000
        )
        values["YearEnd"] = datetime.fromtimestamp(
            values["YearEnd"]["Timestamp"] / 1000
        )
        return values


class Period(BaseModel):
    id: int = Field(alias="Id")
    number: int = Field(alias="Number")
    level: int = Field(alias="Level")
    start: datetime = Field(alias="Start")
    end: datetime = Field(alias="End")
    current: bool = Field(alias="Current")
    last_in_year: bool = Field(alias="Last")
    scopes: list[str] = Field(alias="Capabilities")

    @root_validator(pre=True)
    def root_validator(cls, values):
        values["Start"] = datetime.fromtimestamp(values["Start"]["Timestamp"] / 1000)
        values["End"] = datetime.fromtimestamp(values["End"]["Timestamp"] / 1000)
        return values


class PupilLogin(BaseModel):
    id: int = Field(alias="LoginId")
    value: str = Field(alias="LoginValue")
    first_name: str = Field(alias="FirstName")
    second_name: str = Field(alias="SecondName")
    last_name: str = Field(alias="Surname")
    sex: Sex = Field(alias="Sex")


class MessageBox(BaseModel):
    id: int = Field(alias="Id")
    name: str = Field(alias="Name")
    global_key: str = Field(alias="GlobalKey")


class Pupil(BaseModel):
    id: int = Field(alias="Id")
    team: str = Field(alias="ClassDisplay")
    scopes: list[Scope] = Field(alias="Capabilities")
    unit: Unit = Field(alias="Unit")
    constituent_unit: ConstituentUnit = Field(alias="ConstituentUnit")
    user_login: UserLogin = Field(alias="Login")
    journal: Optional[Journal] = Field(alias="Journal")
    periods: list[Period] = Field(alias="Periods")
    pupil_login: PupilLogin = Field(alias="Pupil")
    message_box: MessageBox = Field(alias="MessageBox")
    context: str = Field(alias="Context")

    @root_validator(pre=True)
    def root_validator(cls, values):
        values["Id"] = values["Pupil"]["Id"]
        values["Unit"]["Group"] = values["TopLevelPartition"]
        return values

    @staticmethod
    async def get(api: API) -> list["Pupil"]:
        envelope, envelope_type = await api.get(
            entity="register/hebe",
            rest_url=api.certificate.rest_url,
            mode=2,
        )
        if envelope_type != "IEnumerable`1":
            raise InvalidResponseEnvelopeTypeException()
        return [Pupil.parse_obj(pupil) for pupil in envelope]
