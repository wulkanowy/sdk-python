from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from sdk_python.efeb.data.employee import Employee
from sdk_python.efeb.models.start import (
    Permissions,
    PermissionsAuthInfo,
    PermissionsUnit,
)
from sdk_python.efeb.models.student import (
    RawRegister,
    RawPeriod,
    RawStudentPersonalData,
    RawSchoolData,
    RawStudentCache,
)


class RegisterType(Enum):
    UNKNOWN = 0
    DEFAULT = 1
    KINDERGARTEN = 2
    PUPILS = 3


class Sex(Enum):
    MAN = True
    WOMAN = False


class Scopes(Enum):
    REGULAR = 0
    TEXTBOOKS = 1
    PLANNED_LESSONS = 2
    REALIZED_LESSONS = 3
    MENU = 4
    OFFICE_ACCESS = 5
    FORMS = 6
    MOBILE_ACCESS = 7
    MEETINGS = 8
    SEMESTER_EXAMS = 9
    ATTENDANCE_RECORDS = 10


class Role(Enum):
    STUDENT = 0
    GUARDIAN = 1


@dataclass
class Pupil:
    first_name: str
    second_name: str
    last_name: str
    sex: Sex
    adult: bool

    def __init__(
        self,
        raw_register: RawRegister,
        raw_student_personal_data: RawStudentPersonalData,
    ):
        self.first_name = raw_student_personal_data.first_name
        self.second_name = raw_student_personal_data.second_name
        self.last_name = raw_student_personal_data.last_name
        self.sex = Sex(raw_student_personal_data.sex)
        self.adult = raw_register.adult


@dataclass
class Unit:
    id: int
    short: str
    symbol: str
    name: str
    address: str
    contact: str
    headmasters: list[Employee]
    pedagogues: list[Employee]
    group: str

    def __init__(
        self,
        permissions: Permissions,
        raw_school_data: RawSchoolData,
        unit_id: int,
        group: str,
    ):
        unit: PermissionsUnit = [
            unit for unit in permissions.units if unit.id == unit_id
        ][0]
        self.id = unit.id
        self.short = unit.short
        self.symbol = unit.symbol
        self.name = unit.name
        self.address = raw_school_data.school.address
        self.contact = raw_school_data.school.contact
        self.headmasters = [Employee(headmaster) for headmaster in raw_school_data.school.headmaster.split(", ")]
        self.pedagogues = [Employee(pedagogue) for pedagogue in raw_school_data.school.pedagogue.split(", ")]
        self.group = group


@dataclass
class Period:
    id: int
    number: int
    level: int
    start: datetime
    end: datetime
    team_id: int
    last_in_year: bool

    def __init__(self, raw_period: RawPeriod):
        self.id = raw_period.id
        self.number = raw_period.number
        self.level = raw_period.level
        self.start = raw_period.start
        self.end = raw_period.end
        self.team_id = raw_period.team_id
        self.last_in_year = raw_period.last_period


@dataclass
class Team:
    level: int
    symbol: str

    def __init__(self, raw_register: RawRegister):
        self.level = raw_register.team_level
        self.symbol = raw_register.team_symbol


@dataclass
class Register:
    id: int
    start: datetime
    end: datetime
    year_id: int
    team: Team
    periods: list[Period]
    scopes: list[Scopes]
    type: RegisterType = RegisterType.UNKNOWN

    def __init__(self, raw_register: RawRegister, raw_student_cache: RawStudentCache):
        self.id = raw_register.register_id
        self.start = raw_register.start
        self.end = raw_register.end
        self.year_id = raw_register.year_id
        self.team = Team(raw_register)
        self.periods = [Period(raw_period) for raw_period in raw_register.periods]
        self.scopes = []
        if raw_register.is_register:
            if raw_register.kindergarten:
                self.type = RegisterType.KINDERGARTEN
                self.scopes.append(Scopes.ATTENDANCE_RECORDS)
                self.scopes.append(Scopes.MEETINGS)
            elif raw_register.pupils:
                self.type = RegisterType.PUPILS
                self.scopes.append(Scopes.ATTENDANCE_RECORDS)
            else:
                self.type = RegisterType.DEFAULT
                self.scopes.append(Scopes.REGULAR)
                self.scopes.append(Scopes.MEETINGS)
                if raw_register.adults:
                    self.scopes.append(Scopes.SEMESTER_EXAMS)
            if raw_register.guardian:
                self.scopes.append(Scopes.FORMS)
        else:
            self.type = RegisterType.UNKNOWN
        if raw_student_cache.menu_enabled:
            self.scopes.append(Scopes.MENU)
        if raw_student_cache.textbooks_enabled:
            self.scopes.append(Scopes.TEXTBOOKS)
        if raw_student_cache.planned_lessons_enabled:
            self.scopes.append(Scopes.PLANNED_LESSONS)
        if raw_student_cache.realized_lessons_enabled:
            self.scopes.append(Scopes.REALIZED_LESSONS)
        if raw_student_cache.office_access_enabled:
            self.scopes.append(Scopes.OFFICE_ACCESS)


@dataclass
class Login:
    id: int
    value: str
    role: Role
    full_name: str
    name: str = None
    last_name: str = None

    def __init__(
        self,
        raw_register: RawRegister,
        full_name: str,
        unit_id: int,
        permissions: Permissions,
        raw_student_personal_data: RawStudentPersonalData,
    ):
        auth_info: PermissionsAuthInfo = [
            auth_info
            for auth_info in permissions.auth_infos
            if auth_info.unit_id == unit_id
        ][0]
        self.id = auth_info.login_id
        self.value = auth_info.login_value
        self.full_name = full_name
        if raw_register.guardian:
            self.role = Role.GUARDIAN
            if raw_student_personal_data.guardian_1.id in auth_info.guardian_ids:
                self.name = raw_student_personal_data.guardian_1.name
                self.last_name = raw_student_personal_data.guardian_1.last_name
            elif raw_student_personal_data.guardian_2.id in auth_info.guardian_ids:
                self.name = raw_student_personal_data.guardian_2.name
                self.last_name = raw_student_personal_data.guardian_2.last_name
        else:
            self.role = Role.STUDENT
            self.name = raw_student_personal_data.first_name
            self.last_name = raw_student_personal_data.last_name


@dataclass
class Student:
    id: int
    registers: list[Register]
    login: Login
    pupil: Pupil
    unit: Unit
    constituent_unit_id: int
    app_guid: str
    app_version: str
    request_verification_token: str
    session_cookies: dict[str, str]

    def __init__(
        self,
        raw_register: RawRegister,
        permissions: Permissions,
        unit_id: int,
        unit_group: str,
        raw_student_personal_data: RawStudentPersonalData,
        login_full_name: str,
        raw_student_cache: RawStudentCache,
        raw_school_data: RawSchoolData,
        app_guid: str,
        app_version: str,
        request_verification_token: str,
        session_cookies: dict[str, str],
    ):
        self.id = raw_register.student_id
        self.registers = [Register(raw_register, raw_student_cache)]
        self.login = Login(
            raw_register,
            login_full_name,
            unit_id,
            permissions,
            raw_student_personal_data,
        )
        self.pupil = Pupil(raw_register, raw_student_personal_data)
        self.unit = Unit(permissions, raw_school_data, unit_id, unit_group)
        self.constituent_unit_id = raw_register.constituent_unit_id
        self.app_guid = app_guid
        self.app_version = app_version
        self.request_verification_token = request_verification_token
        self.session_cookies = session_cookies
