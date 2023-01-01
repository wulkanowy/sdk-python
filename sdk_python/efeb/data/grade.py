import re
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from sdk_python.efeb.data.employee import Employee
from sdk_python.efeb.data.student import RegisterType
from sdk_python.efeb.models.student import RawGrade, RawGradesSubject, RawGradesData
from sdk_python.efeb.session import Session
from sdk_python.efeb.utils import get_student_cookies


class GradeColumnColor(Enum):
    BLACK = 0
    GREEN = 7261447
    PURPLE = 11627761
    RED = 15748172
    BLUE = 2139383

@dataclass
class GradeColumnSubject:
    name: str
    position: int

    def __init__(self, raw_grades_subject: RawGradesSubject):
        self.name = raw_grades_subject.name
        self.position = raw_grades_subject.position

@dataclass
class GradeColumn:
    code: str
    name: str
    subject: GradeColumnSubject
    weight: float
    color: GradeColumnColor

    def __init__(self, raw_grades_subject: RawGradesSubject, raw_grade: RawGrade):
        self.code = raw_grade.column_code
        self.name = raw_grade.column_name
        self.subject = GradeColumnSubject(raw_grades_subject)
        self.weight = raw_grade.weight
        self.color = GradeColumnColor(raw_grade.color)

@dataclass
class Grade:
    entry: str
    teacher: Employee
    date: datetime
    column: GradeColumn
    comment: str = None

    def __init__(self, raw_grades_subject: RawGradesSubject, raw_grade: RawGrade):
        try:
            self.comment = re.search("\((.+?)\)", raw_grade.entry).group(1)
            self.entry = re.search("(.+?)\(", raw_grade.entry).group(1)
        except AttributeError:
            self.entry = raw_grade.entry
        self.teacher = Employee(raw_grade.teacher)
        self.date = raw_grade.date
        self.column = GradeColumn(raw_grades_subject, raw_grade)

    @staticmethod
    async def get(
            scheme: str,
            host: str,
            units_group: str,
            unit_symbol: str,
            student_id: int,
            register_id: int,
            register_type: RegisterType,
            year_id: int,
            session_cookies: dict[str, str],
            period_id: int
    ) -> list["RawGradesData"]:
        session: Session = Session()
        cookies: dict[str, str] = get_student_cookies(
            student_id, register_id, register_type, year_id
        )
        cookies.update(session_cookies)
        data: dict = await session.student_request(
            scheme, host, units_group, unit_symbol, "Oceny.mvc/Get", cookies=cookies, data={"okres": period_id}
        )
        raw_grades_data: RawGradesData = RawGradesData(data)
        grades: list[Grade] = []
        for raw_subject in raw_grades_data.subjects:
            for raw_grade in raw_subject.grades:
                grades.append(Grade(raw_subject, raw_grade))
        return grades
