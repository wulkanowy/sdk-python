from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class RawMeeting:
    title: str
    subject: str
    agenda: str
    present_guardians: str
    date: datetime
    online: Any
    id: int

    def __init__(self, data: dict):
        self.title = data["Tytul"]
        self.subject = data["TematZebrania"]
        self.agenda = data["Agenda"]
        self.present_guardians = data["ObecniNaZebraniu"]
        self.date = data["DataSpotkania"]
        self.online = data["ZebranieOnline"]
        self.id = data["Id"]
