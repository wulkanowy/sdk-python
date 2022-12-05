from dataclasses import dataclass
from datetime import datetime


@dataclass
class RawPeriod:
    number: int
    level: int
    start: datetime
    end: datetime
    team_id: int
    unit_id: int
    last_period: bool
    id: int

    def __init__(self, data: dict):
        self.number = data["NumerOkresu"]
        self.level = data["Poziom"]
        self.start = datetime.fromisoformat(data["DataOd"])
        self.end = datetime.fromisoformat(data["DataDo"])
        self.team_id = data["IdOddzial"]
        self.unit_id = data["IdJednostkaSprawozdawcza"]
        self.last_period = data["IsLastOkres"]
        self.id = data["Id"]


@dataclass
class RawRegister:
    id: int
    student_id: int
    student_name: str
    student_second_name: str
    student_last_name: str
    is_register: bool
    register_id: int
    kindergarten_register_id: int
    pupils_register_id: int
    team_level: int
    team_symbol: str
    year_id: int
    periods: list[RawPeriod]
    start: datetime
    end: datetime
    constituent_unit_id: int
    sio_type_id: int
    adults: bool
    post_secondary: bool
    _13: bool
    artistic: bool
    artistic_13: bool
    special: bool
    kindergarten: bool
    pupils: bool
    archived: bool
    full_name: str
    adult: bool
    parent: bool
    authorized: bool
    citizenship: int

    def __init__(self, data: dict):
        self.id = data["Id"]
        self.student_id = data["IdUczen"]
        self.student_name = data["UczenImie"]
        self.student_second_name = data["UczenImie2"]
        self.student_last_name = data["UczenNazwisko"]
        self.is_register = data["IsDziennik"]
        self.register_id = data["IdDziennik"]
        self.kindergarten_register_id = data["IdPrzedszkoleDziennik"]
        self.pupils_register_id = data["IdWychowankowieDziennik"]
        self.team_level = data["Poziom"]
        self.team_symbol = data["Symbol"]
        self.year_id = data["DziennikRokSzkolny"]
        self.periods = [RawPeriod(period_data) for period_data in data["Okresy"]]
        self.start = datetime.fromisoformat(data["DziennikDataOd"])
        self.end = datetime.fromisoformat(data["DziennikDataDo"])
        self.constituent_unit_id = data["IdJednostkaSkladowa"]
        self.sio_type_id = data["IdSioTyp"]
        self.adults = data["IsDorosli"]
        self.post_secondary = data["IsPolicealna"]
        self._13 = data["Is13"]
        self.artistic = data["IsArtystyczna"]
        self.artistic_13 = data["IsArtystyczna13"]
        self.special = data["IsSpecjalny"]
        self.kindergarten = data["IsPrzedszkola"]
        self.pupils = data["IsWychowankowie"]
        self.archived = data["IsArchiwalny"]
        self.full_name = data["UczenPelnaNazwa"]
        self.adult = data["IsAdult"]
        self.guardian = data["IsStudentParent"]
        self.authorized = data["IsAuthorized"]
        self.citizenship = data["Obywatelstwo"]
