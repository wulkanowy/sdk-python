from dataclasses import dataclass
import re

@dataclass
class Employee:
    full_name: str
    name: str = None
    initials: str = None

    def __init__(self, full_name: str):
        try:
            self.name = re.search("(.+?) \[", full_name).group(1)
            self.initials = re.search(" \[(.+?)\]", full_name).group(1)
        except AttributeError:
            pass
        self.full_name = full_name