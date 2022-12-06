import json
from base64 import b64decode

from uonet_fslogin import UonetFSLogin

from sdk_python.efeb.data import Student, Register
from sdk_python.efeb.models.start import Permissions
from sdk_python.efeb.models.student import RawStudentCache, RawRegister, RawSchoolData, RawStudentPersonalData
from sdk_python.efeb.session import Session
from sdk_python.efeb.utils import get_login_name, get_script_param, get_student_headers


class Client:

    def __init__(self, scheme: str, host: str, sessions: dict[str, dict[str, str]] = None):
        self.scheme: str = scheme
        self.host = host
        self.http_session = Session()
        self.sessions = sessions

    async def log_in(self, username: str, password: str, **kwargs) -> dict[str, dict[str, str]]:
        uonet_fslogin: UonetFSLogin = UonetFSLogin(self.scheme, self.host)
        sessions, user_data = await uonet_fslogin.log_in(username, password, **kwargs)
        self.sessions = sessions
        return user_data

    async def get_students(self) -> list[Student]:
        students: list[Student] = []
        for units_group in self.sessions:
            self.http_session.session.cookie_jar.clear()
            self.http_session.session.cookie_jar.update_cookies(self.sessions[units_group])
            start_page: str = await self.http_session.request(
                method="GET",
                url=f"{self.scheme}://uonetplus.{self.host}/{units_group}/Start.mvc/Index")
            login_name: str = get_login_name(start_page)
            permissions = Permissions(json.loads(b64decode(get_script_param(start_page, "permissions").split("|")[0])))
            for unit in permissions.units:
                student_start: str = await self.http_session.request(
                    method="GET",
                    url=f'{self.scheme}://uonetplus-uczen.{self.host}/{units_group}/{unit.symbol}/LoginEndpoint.aspx',
                )
                session_cookies: dict[str, str] = {}
                for cookie in self.http_session.session.cookie_jar:
                    session_cookies[cookie.key] = cookie.value
                app_guid: str = get_script_param(student_start, "appGuid")
                app_version: str = get_script_param(student_start, "version")
                request_verification_token: str = get_script_param(student_start, "antiForgeryToken")
                headers: dict[str, str] = get_student_headers(student_start)
                self.http_session.session.headers.update(headers)
                raw_student_cache = RawStudentCache(await self.http_session.student_request(
                    self.scheme, self.host, units_group, unit.symbol, "UczenCache.mvc/Get"
                ))
                raw_registers = [RawRegister(raw_register) for raw_register in await self.http_session.student_request(
                    self.scheme, self.host, units_group, unit.symbol, "UczenDziennik.mvc/Get"
                )]
                for raw_register in raw_registers:
                    cookies: dict[str, str] = {
                        "idBiezacyDziennik": str(raw_register.register_id),
                        "idBiezacyDziennikPrzedszkole": str(raw_register.kindergarten_register_id),
                        "idBiezacyDziennikWychowankowie": str(raw_register.pupils_register_id),
                        "idBiezacyUczen": str(raw_register.student_id),
                        "biezacyRokSzkolny": str(raw_register.year_id)
                    }
                    self.http_session.session.cookie_jar.update_cookies(cookies)
                    if not [student for student in students if
                            student.id == raw_register.student_id and
                            student.unit.id == unit.id and student.unit.group == units_group]:
                        raw_school_data: RawSchoolData = RawSchoolData(await self.http_session.student_request(
                            self.scheme, self.host, units_group, unit.symbol, "SzkolaINauczyciele.mvc/Get",
                            cookies=cookies
                        ))
                        raw_student_personal_data: RawStudentPersonalData = RawStudentPersonalData(
                            await self.http_session.student_request(
                                self.scheme, self.host, units_group, unit.symbol, "Uczen.mvc/Get", cookies=cookies
                            ))
                        students.append(
                            Student(raw_register, permissions, unit.id, units_group, raw_student_personal_data,
                                    login_name, raw_student_cache, raw_school_data, app_guid, app_version,
                                    request_verification_token, session_cookies)
                        )
                    else:
                        register = Register(raw_register, raw_student_cache)
                        students[students.index(
                            [student for student in students if student.id == raw_register.student_id
                             and student.unit.id == unit.id and student.unit.group == units_group][0])] \
                            .registers.append(register)
            return students
