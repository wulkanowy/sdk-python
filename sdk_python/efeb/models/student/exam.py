from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class RawExam:
    subject: str
    teacher: str
    entry_date: datetime
    start_hour: Any
    duration: Any
    description: str
    type: int
    urls: list[Any]
    id: int

    def __init__(self, data: dict):
        self.subject = data["Nazwa"]
        self.teacher = data["Pracownik"]
        self.entry_date = datetime.fromisoformat(data["DataModyfikacji"])
        self.start_hour = data["GodzinaOd"]
        self.duration = data["CzasTrwania"]
        self.description = data["Opis"]
        self.type = data["Rodzaj"]
        self.urls = data["SprawdzianUrls"]
        self.id = data["Id"]


@dataclass
class RawExamsDay:
    date: datetime
    exams: list[RawExam]
    show: bool

    def __init__(self, data: dict):
        self.date = datetime.fromisoformat(data["Data"])
        self.exams = [RawExam(exam_data) for exam_data in data["Sprawdziany"]]
        self.show = data["Pokazuj"]


@dataclass
class RawExamsWeek:
    days: list[RawExamsDay]

    def __init__(self, data: dict):
        self.days = [RawExamsDay(day_data) for day_data in data["SprawdzianyGroupedByDayList"]]
