from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from sdk_python.hebe.api import API


class Teacher(BaseModel):
    id: int = Field(alias="Id")
    name: Optional[str] = Field(alias="Name")
    last_name: Optional[str] = Field(alias="Surname")
    full_name: str = Field(alias="DisplayName")
    position: int = Field(alias="Position")
    description: str = Field(alias="Description")

    @staticmethod
    async def get_by_pupil_and_period(
        api: API,
        pupil_id: int,
        period_id: int,
        last_sync_date: datetime = datetime.min,
        return_other_employees: bool = False,
    ) -> list["Teacher"]:
        envelope = await api.get_all(
            "teacher/byPeriod",
            {
                "pupilId": pupil_id,
                "periodId": period_id,
                "lastSyncDate": last_sync_date.isoformat(),
            },
        )
        return list(
            map(
                Teacher.parse_obj,
                filter(
                    lambda teacher: teacher["Position"] == 1 or return_other_employees,
                    envelope,
                ),
            )
        )
