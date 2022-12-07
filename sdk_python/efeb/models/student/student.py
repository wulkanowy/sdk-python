from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class RawGuardianPersonalData:
    id: int
    name: str
    last_name: str
    kinship: str
    address: str
    home_phone: str
    cell_phone: str
    work_phone: str
    email_address: str
    full_name: str
    phones: str

    def __init__(self, data: dict):
        self.id = data["Id"]
        self.name = data["Imie"]
        self.last_name = data["Nazwisko"]
        self.kinship = data["StPokrewienstwa"]
        self.address = data["Adres"]
        self.home_phone = data["TelDomowy"]
        self.cell_phone = data["TelKomorkowy"]
        self.work_phone = data["TelSluzbowy"]
        self.email_address = data["Email"]
        self.phone = data["Telefon"]


@dataclass
class RawStudentPersonalData:
    first_name: str
    second_name: str
    document_number: Any
    last_name: str
    brith_date: datetime
    brith_place: str
    family_name: str
    polish_citizenship: int
    mother_name: str
    father_name: str
    sex: bool
    home_address: str
    registered_address: str
    correspondence_address: str
    home_phone: str
    cell_phone: str
    email_address: str
    show_pesel: bool
    guardian_1: RawGuardianPersonalData
    guardian_2: RawGuardianPersonalData
    hide_address_data: bool
    full_name: str
    has_pesel: bool
    pole: bool
    mother_and_father_name: str
    show_photo: bool

    def __init__(self, data: dict):
        self.first_name = data["Imie"]
        self.second_name = data["Imie2"]
        self.document_number = data["NumerDokumentu"]
        self.last_name = data["Nazwisko"]
        self.brith_date = datetime.fromisoformat(data["DataUrodzenia"])
        self.brith_place = data["MiejsceUrodzenia"]
        self.family_name = data["NazwiskoRodowe"]
        self.polish_citizenship = data["ObywatelstwoPolskie"]
        self.mother_name = data["ImieMatki"]
        self.father_name = data["ImieOjca"]
        self.sex = data["Plec"]
        self.home_address = data["AdresZamieszkania"]
        self.registered_address = data["AdresZameldowania"]
        self.correspondence_address = data["AdresKorespondencji"]
        self.home_phone = data["TelDomowy"]
        self.cell_phone = data["TelKomorkowy"]
        self.email_address = data["Email"]
        self.show_pesel = data["CzyWidocznyPesel"]
        self.guardian_1 = (
            RawGuardianPersonalData(data["Opiekun1"]) if data["Opiekun1"] else None
        )
        self.guardian_2 = (
            RawGuardianPersonalData(data["Opiekun2"]) if data["Opiekun2"] else None
        )
        self.full_name = data["ImieNazwisko"]
        self.has_pesel = data["PosiadaPesel"]
        self.pole = data["Polak"]
        self.mother_and_father_name = data["ImieMatkiIOjca"]
        self.show_photo = data["ShowPhoto"]
