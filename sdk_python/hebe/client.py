from datetime import date

from sdk_python.hebe import Certificate
from sdk_python.hebe.api import API
from sdk_python.hebe.data.exam import Exam
from sdk_python.hebe.data.grade import Grade, GradesSummary
from sdk_python.hebe.data.homework import Homework
from sdk_python.hebe.data.lucky_number import LuckyNumber
from sdk_python.hebe.data.meeting import Meeting
from sdk_python.hebe.data.note import Note
from sdk_python.hebe.data.pupil import PupilInfo, Pupil
from sdk_python.hebe.data.time_slot import TimeSlot


class Client:
    def __init__(self, api: API):
        self._api = api

    @staticmethod
    async def register_certificate(
        certificate: Certificate, token: str, symbol: str, pin: str, **kwargs
    ) -> None:
        await certificate.register(token, symbol, pin, **kwargs)

    async def get_pupils_infos(self, **kwargs) -> list[PupilInfo]:
        return await PupilInfo.get(self._api, **kwargs)

    async def get_pupil_by_id(self, pupil_id: int) -> Pupil:
        return await Pupil.get_by_id(self._api, pupil_id)

    async def get_lucky_number_by_constituent_unit(
        self, constituent_unit_id: int, day: date = date.today()
    ) -> LuckyNumber:
        return await LuckyNumber.get_by_constituent_unit(
            self._api, constituent_unit_id, day
        )

    async def get_time_slots(self) -> list[TimeSlot]:
        return await TimeSlot.get(self._api)

    async def get_grades_by_pupil_and_period(
        self, pupil_id: int, period_id: int, behaviour: bool = False, **kwargs
    ) -> list[Grade]:
        return await Grade.get_by_pupil_and_period(
            self._api, pupil_id, period_id, behaviour, **kwargs
        )

    async def get_grade_by_pupil_period_and_id(
        self, pupil_id: int, period_id: int, grade_id: int
    ) -> Grade:
        return await Grade.get_by_pupil_period_and_id(
            self._api, pupil_id, period_id, grade_id
        )

    async def get_deleted_grades_by_pupil_and_period(
        self, pupil_id: int, period_id: int, **kwargs
    ) -> list[int]:
        return await Grade.get_deleted_by_pupil_and_period(
            self._api, pupil_id, period_id, **kwargs
        )

    async def get_deleted_grades(self, **kwargs) -> list[int]:
        return await Grade.get_deleted(self._api, **kwargs)

    async def get_grades_summary_by_pupil_and_period(
        self, pupil_id: int, period_id: int
    ) -> list[GradesSummary]:
        return await GradesSummary.get_by_pupil_and_period(
            self._api, pupil_id, period_id
        )

    async def get_notes_by_pupil(self, pupil_id: int, **kwargs) -> list[Note]:
        return await Note.get_by_pupil(self._api, pupil_id, **kwargs)

    async def get_note_by_pupil_and_id(self, pupil_id: int, note_id: int) -> Note:
        return await Note.get_by_pupil_and_id(self._api, pupil_id, note_id)

    async def get_deleted_notes_by_pupil(self, pupil_id: int, **kwargs) -> list[int]:
        return await Note.get_deleted_by_pupil(self._api, pupil_id, **kwargs)

    async def get_meetings_by_pupil(
        self, pupil_id: int, from_date: date, **kwargs
    ) -> list[Meeting]:
        return await Meeting.get_by_pupil(self._api, pupil_id, from_date, **kwargs)

    async def get_meeting_by_pupil_and_id(
        self, pupil_id: int, meeting_id: int
    ) -> Meeting:
        return await Meeting.get_by_pupil_and_id(self._api, pupil_id, meeting_id)

    async def get_deleted_meetings_by_pupil(self, pupil_id: int, **kwargs) -> list[int]:
        return await Meeting.get_deleted_by_pupil(self._api, pupil_id, **kwargs)

    async def get_exams_by_pupil(self, pupil_id: int, **kwargs) -> list[Exam]:
        return await Exam.get_by_pupil(self._api, pupil_id, **kwargs)

    async def get_exam_by_pupil_and_id(self, pupil_id: int, exam_id: int) -> Exam:
        return await Exam.get_by_pupil_and_id(self._api, pupil_id, exam_id)

    async def get_deleted_exams(self, **kwargs) -> list[int]:
        return await Exam.get_deleted(self._api, **kwargs)

    async def get_deleted_exams_by_pupil(self, pupil_id: int, **kwargs) -> list[int]:
        return await Exam.get_deleted_by_pupil(self._api, pupil_id, **kwargs)

    async def get_homework_by_pupil(self, pupil_id: int, **kwargs) -> list[Homework]:
        return await Homework.get_by_pupil(self._api, pupil_id, **kwargs)

    async def get_deleted_homework(self, **kwargs) -> list[int]:
        return await Homework.get_deleted(self._api, **kwargs)

    async def get_deleted_homework_by_pupil(self, pupil_id: int, **kwargs) -> list[int]:
        return await Homework.get_deleted_by_pupil(self._api, pupil_id, **kwargs)
