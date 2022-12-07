from __future__ import annotations

import json
from logging import getLogger
from typing import Union

import aiohttp

from sdk_python.efeb.error import (
    UnsuccessfulStudentResponseException,
    InvalidStudentResponseException,
)
from sdk_python.efeb.models.student.response import StudentResponse


class Session:
    def __init__(self):
        self.session = aiohttp.ClientSession()
        self.log = getLogger(__name__)

    async def request(self, url: str, method: str, **kwargs) -> str:
        async with self.session.request(url=url, method=method, **kwargs) as response:
            for res in response.history:
                self.log.debug(f"{res.method} {res.status} {res.url}")
            self.log.debug(f"{response.method} {response.status} {response.url}")
            content: str = await response.text()
        return content

    async def student_request(
        self,
        scheme: str,
        host: str,
        units_group: str,
        unit_symbol: str,
        endpoint: str,
        method: str = "POST",
        **kwargs,
    ) -> Union[str, dict, list, bool]:
        url: str = (
            f"{scheme}://uonetplus-uczen.{host}/{units_group}/{unit_symbol}/{endpoint}"
        )
        response_content: str = await self.request(url, method, **kwargs)
        try:
            response_json: StudentResponse = StudentResponse(
                json.loads(response_content)
            )
        except:
            raise InvalidStudentResponseException
        if not response_json.success:
            raise UnsuccessfulStudentResponseException
        return response_json.data
