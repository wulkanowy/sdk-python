from dataclasses import dataclass
from datetime import datetime
from typing import Any

from sdk_python.efeb.data.student import RegisterType
from sdk_python.efeb.models.student import RawMeeting
from sdk_python.efeb.session import Session
from sdk_python.efeb.utils import get_student_cookies


@dataclass
class Meeting:
    id: int
    subject: str
    date: datetime
    agenda: str
    online: Any
    present_guardians: str
    place: str = None

    def __init__(self, raw_meeting: RawMeeting):
        self.id = raw_meeting.id
        self.subject = raw_meeting.subject
        self.date = raw_meeting.date
        if len(raw_meeting.title.split(", ")) > 2:
            self.place = raw_meeting.title.split(", ")[2]
        self.agenda = raw_meeting.agenda
        self.online = raw_meeting.online
        self.present_guardians = raw_meeting.present_guardians

    @staticmethod
    async def get(scheme: str, host: str, units_group: str, unit_symbol: str, student_id: int, register_id: int,
                  register_type: RegisterType, year_id: int, session_cookies: dict[str, str]) -> list["Meeting"]:
        session: Session = Session()
        cookies: dict[str, str] = get_student_cookies(student_id, register_id, register_type, year_id)
        cookies.update(session_cookies)
        data: list[RawMeeting] = [RawMeeting(data) for data in
                                  await session.student_request(scheme, host, units_group, unit_symbol,
                                                                "Zebrania.mvc/Get", cookies=cookies)]
        meetings: list["Meeting"] = [Meeting(raw_meeting) for raw_meeting in data]
        return meetings
