from dataclasses import dataclass

@dataclass
class StudentResponse:
    success: bool
    data: dict

    def __init__(self, raw_response: dict):
        self.success = raw_response["success"]
        if "data" in raw_response:
            self.data = raw_response["data"]
