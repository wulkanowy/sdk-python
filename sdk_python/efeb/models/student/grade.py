from dataclasses import dataclass
from datetime import datetime

@dataclass
class RawGrade:
    teacher: str
    entry: str
    weight: float
    column_name: str
    column_short: str
    date: datetime
    color: int

    def __init__(self, data: dict):
        self.teacher = data["Nauczyciel"]
        self.entry = data["Wpis"]
        self.weight = data["Waga"]
        self.column_name = data["NazwaKolumny"]
        self.column_code = data["KodKolumny"]
        self.date = datetime.strptime(data["DataOceny"], "%d.%m.%Y")
        self.color = data["KolorOceny"]

@dataclass
class RawGradesSubject:
    name: str
    position: int
    grades: list[RawGrade]
    proposed_period_grade: str
    final_period_grade: str
    proposed_period_points_grade: str
    final_period_points_grade: str
    average: float
    total_points: str
    visible: bool

    def __init__(self, data: dict):
        self.name = data["Przedmiot"]
        self.position = data["Pozycja"]
        self.grades = [RawGrade(grade_data) for grade_data in data["OcenyCzastkowe"]]
        self.proposed_period_grade = data["ProponowanaOcenaRoczna"]
        self.final_period_grade = data["OcenaRoczna"]
        self.proposed_period_points_grade = data["ProponowanaOcenaRocznaPunkty"]
        self.final_period_points_grade = data["OcenaRocznaPunkty"]
        self.average = data["Srednia"]
        self.total_points = data["SumaPunktow"]
        self.visible = data["WidocznyPrzedmiot"]

@dataclass
class RawDescriptiveGrade:
    subject: str
    description: str
    religion_or_ethic: bool

    def __init__(self, data: dict):
        self.subject = data["NazwaPrzedmiotu"]
        self.description = data["Opis"]
        self.religion_or_ethic = data["IsReligiaEtyka"]


@dataclass
class RawGradesData:
    average_enabled: bool
    points_grades_enabled: bool
    subjects: list[RawGradesSubject]
    descriptive_grades: list[RawDescriptiveGrade]
    grades_type: int
    last_period_in_year: bool
    for_adults: bool

    def __init__(self, data: dict):
        self.average_enabled = data["IsSrednia"]
        self.points_grades_enabled = data["IsPunkty"]
        self.subjects = [RawGradesSubject(subject_data) for subject_data in data["Oceny"]]
        self.descriptive_grades = [RawDescriptiveGrade(descriptive_grade_data) for descriptive_grade_data in data["OcenyOpisowe"]]
        self.grades_type = data["TypOcen"]
        self.last_period_in_year = data["IsOstatniSemestr"]
        self.for_adults = data["IsDlaDoroslych"]