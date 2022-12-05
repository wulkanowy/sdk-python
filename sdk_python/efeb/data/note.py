from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from sdk_python.efeb.data import RegisterType
from sdk_python.efeb.models.student import RawNote, RawNotesAndAchievements
from sdk_python.efeb.session import Session
from sdk_python.efeb.utils import get_student_cookies


class NoteCategoryType(Enum):
    UNKNOWN = 0
    POSITIVE = 1
    NEUTRAL = 2
    NEGATIVE = 3


@dataclass
class NoteCategory:
    name: str
    type: NoteCategoryType

    def __init__(self, raw_note: RawNote):
        self.name = raw_note.category_name
        self.type = NoteCategoryType(raw_note.category_type)


@dataclass
class Note:
    content: str
    teacher: str
    points: str
    category: NoteCategory
    date: datetime

    def __init__(self, raw_note: RawNote):
        self.content = raw_note.content
        self.teacher = raw_note.teacher
        self.points = raw_note.points
        self.category = NoteCategory(raw_note)
        self.date = raw_note.date

    @staticmethod
    async def get(scheme: str, host: str, units_group: str, unit_symbol: str, student_id: int, register_id: int,
                  register_type: RegisterType, year_id: int, session_cookies: dict[str, str]) -> list["Note"]:
        session: Session = Session()
        cookies: dict[str, str] = get_student_cookies(student_id, register_id, register_type, year_id)
        cookies.update(session_cookies)
        data: RawNotesAndAchievements = RawNotesAndAchievements(
            await session.student_request(scheme, host, units_group, unit_symbol, "UwagiIOsiagniecia.mvc/Get",
                                          cookies=cookies))
        notes: list["Note"] = [Note(raw_note) for raw_note in data.notes]
        return notes


@dataclass
class Achievement:
    content: str

    @staticmethod
    async def get(scheme: str, host: str, units_group: str, unit_symbol: str, student_id: int, register_id: int,
                  register_type: RegisterType, year_id: int, session_cookies: dict[str, str]) -> list["Achievements"]:
        session: Session = Session()
        cookies: dict[str, str] = get_student_cookies(student_id, register_id, register_type, year_id)
        cookies.update(session_cookies)
        data: RawNotesAndAchievements = RawNotesAndAchievements(
            await session.student_request(scheme, host, units_group, unit_symbol, "UwagiIOsiagniecia.mvc/Get",
                                          cookies=cookies))
        achievements: list["Achievement"] = [Achievement(achievement) for achievement in data.achievements]
        return achievements
