from __future__ import annotations

import json
import re
from base64 import b64decode

from bs4 import BeautifulSoup

from sdk_python.efeb.data.student import RegisterType

USER_AGENT: str = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0"
)


def get_script_param(text: str, param: str, default: str = None) -> str:
    m = re.search(f"{param}: '(.+?)'", text)
    return m.group(1) if m else default


def get_student_headers(text: str) -> dict[str, str]:
    app_guid: str = get_script_param(text, "appGuid")
    app_version: str = get_script_param(text, "version")
    request_verification_token: str = get_script_param(text, "antiForgeryToken")
    headers: dict[str, str] = {
        "User-Agent": USER_AGENT,
        "X-V-AppGuid": app_guid,
        "X-V-AppVersion": app_version,
        "X-V-RequestVerificationToken": request_verification_token,
    }
    return headers


def get_student_cookies(
    student_id: int, register_id: int, register_type: RegisterType, year_id: int
) -> dict[str, str]:
    cookies: dict[str, str] = {
        "idBiezacyUczen": str(student_id),
        f'idBiezacyDziennik{"Przedszkole" if register_type is register_type.KINDERGARTEN else ""}{"Wychowankowie" if register_type is register_type.PUPILS else ""}': str(
            register_id
        ),
        "biezacyRokSzkolny": str(year_id),
    }
    return cookies


def get_units_from_permissions(permissions: str):
    decoded_data: dict = json.loads(b64decode(permissions))
    return decoded_data


def get_login_name(start_page: str) -> str:
    bs = BeautifulSoup(start_page, "html.parser")
    user_data_tag = bs.select_one("span.userdata")
    login_name: str = user_data_tag.text.split(" - ")[0]
    return login_name
