from dataclasses import dataclass
from datetime import datetime


@dataclass
class RawNote:
    content: str
    category_name: str
    date: datetime
    teacher: str
    points: str
    show_points: bool
    category_type: int

    def __init__(self, data: dict):
        self.content = data["TrescUwagi"]
        self.category_name = data["Kategoria"]
        self.date = datetime.fromisoformat(data["DataWpisu"])
        self.teacher = data["Nauczyciel"]
        self.points = data["Punkty"]
        self.show_points = data["PokazPunkty"]
        self.category_type = data["KategoriaTyp"]


@dataclass
class RawNotesAndAchievements:
    notes: list[RawNote]
    achievements: list[str]

    def __init__(self, data: dict):
        self.notes = [RawNote(note_data) for note_data in data["Uwagi"]]
        self.achievements = data["Osiagniecia"]
