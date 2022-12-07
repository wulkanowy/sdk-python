from dataclasses import dataclass
from typing import Any


@dataclass
class PermissionsUnit:
    id: int
    name: str
    number: Any
    short: str
    symbol: str
    active: bool
    symbol_integ: Any
    global_key: str

    def __init__(self, data: dict):
        self.id = data["Id"]
        self.name = data["Nazwa"]
        self.number = data["Numer"]
        self.short = data["Skrot"]
        self.symbol = data["Symbol"]
        self.active = data["Aktywna"]
        self.symbol_integ = data["SymbolInteg"]
        self.global_key = data["GlobalKey"]


@dataclass
class PermissionsAuthInfo:
    unit_id: int
    login_id: int
    login_value: str
    student_ids: list[int]
    guardian_ids: list[int]
    employee_ids: list[int]
    roles: list[int]
    linked_account_uids: list[int]

    def __init__(self, data: dict):
        self.unit_id = data["JednostkaSprawozdawczaId"]
        self.login_id = data["LoginId"]
        self.login_value = data["LoginValue"]
        self.student_ids = data["UczenIds"]
        self.guardian_ids = data["OpiekunIds"]
        self.employee_ids = data["PracownikIds"]
        self.roles = data["Roles"]
        self.linked_accounts_uids = data["LinkedAccountUids"]


@dataclass
class Permissions:
    units: list[PermissionsUnit]
    auth_infos: list[PermissionsAuthInfo]

    def __init__(self, data: dict):
        self.units = [PermissionsUnit(unit_data) for unit_data in data["Units"]]
        self.auth_infos = [
            PermissionsAuthInfo(auth_info) for auth_info in data["AuthInfos"]
        ]
