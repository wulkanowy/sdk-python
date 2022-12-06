from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

from sdk_python.efeb.data.student import RegisterType
from sdk_python.efeb.models.student import RawExam, RawExamsDay, RawExamsWeek
from sdk_python.efeb.session import Session
from sdk_python.efeb.utils import get_student_cookies


class ExamType(Enum):
    TEST = 1
    QUIZ = 2
    CLASSWORK = 3


@dataclass
class Exam:
    id: int
    type: ExamType
    subject: str
    description: str
    teacher: str
    date: datetime
    entry_date: datetime

    def __init__(self, raw_exam: RawExam, raw_exams_day: RawExamsDay):
        self.id = raw_exam.id
        self.type = ExamType(raw_exam.type)
        self.subject = raw_exam.subject
        self.description = raw_exam.description
        self.teacher = raw_exam.teacher
        self.date = raw_exams_day.date
        self.entry_date = raw_exam.entry_date

    @staticmethod
    async def get(scheme: str, host: str, units_group: str, unit_symbol: str, student_id: int, register_id: int,
                  register_type: RegisterType, year_id: int, session_cookies: dict[str, str], start: datetime,
                  end: datetime) -> list["Exam"]:
        exams: list[Exam] = []
        session: Session = Session()
        cookies: dict[str, str] = get_student_cookies(student_id, register_id, register_type, year_id)
        cookies.update(session_cookies)
        date: datetime = start
        while True:
            raw_exams_weeks: list[RawExamsWeek] = [RawExamsWeek(data) for data in
                                                   await session.student_request(scheme, host, units_group, unit_symbol,
                                                                                 "Sprawdziany.mvc/Get", cookies=cookies,
                                                                                 data={"data": date.isoformat(),
                                                                                       "rokSzkolny": year_id})]
            for raw_exams_week in raw_exams_weeks:
                for raw_exams_day in raw_exams_week.days:
                    if raw_exams_day.date >= start and raw_exams_day.date <= end:
                        for raw_exam in raw_exams_day.exams:
                            exams.append(Exam(raw_exam, raw_exams_day))
            date = date + timedelta(weeks=4)
            if date > end:
                break
        return exams
