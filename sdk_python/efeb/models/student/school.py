from dataclasses import dataclass


@dataclass
class RawSchool:
    name: str
    address: str
    contact: str
    headmaster: str
    pedagogue: str
    id: int

    def __init__(self, data: dict):
        self.name = data["Nazwa"]
        self.address = data["Adres"]
        self.contact = data["Kontakt"]
        self.headmaster = data["Dyrektor"]
        self.pedagogue = data["Pedagog"]
        self.id = data["Id"]


@dataclass
class RawSubject:
    name: str
    teacher: str
    id: int

    def __init__(self, data: dict):
        self.name = data["Nazwa"]
        self.teacher = data["Nauczyciel"]
        self.id = data["Id"]


@dataclass
class RawSchoolData:
    school: RawSchool
    subjects: list[RawSubject]
    team_name: str

    def __init__(self, data: dict):
        self.school = RawSchool(data["Szkola"])
        self.subjects = [
            RawSubject(subject_data) for subject_data in data["Nauczyciele"]
        ]
        self.team_name = data["Klasa"]
