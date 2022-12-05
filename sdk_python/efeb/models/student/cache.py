from dataclasses import dataclass
from datetime import datetime


@dataclass
class RawStudentCache:
    realized_lessons_enabled: bool
    planned_lessons_enabled: bool
    server_date: datetime
    parent_user: bool
    pupil_user: bool
    menu_enabled: bool
    office_access_enabled: bool
    one_drive_client_id: str
    google_drive_client_id: str
    google_drive_api_key: str
    textbooks_enabled: bool

    def __init__(self, data: dict):
        self.realized_lessons_enabled = data["pokazLekcjeZrealizowane"]
        self.planned_lessons_enabled = data["pokazLekcjeZaplanowane"]
        self.server_date = datetime.fromisoformat(data["serverDate"])
        self.parent_user = data["isParentUser"]
        self.pupil_user = data["isPupilUser"]
        self.menu_enabled = data["isMenuOn"]
        self.office_access_enabled = data["isDostepOffice"]
        self.one_drive_client_id = data["oneDriveClientId"]
        self.google_drive_client_id = data["googleDriveClientId"]
        self.google_drive_api_key = data["googleDriveApiKey"]
        self.textbooks_enabled = data["isPodrecznikiOn"]
