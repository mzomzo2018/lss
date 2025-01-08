from dataclasses import dataclass
from typing import List
from datetime import datetime

@dataclass
class Driver:
    name: str
    version: str
    release_date: datetime

    def __init__(self):
        pass


    def get_id(self) -> int:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_version(self) -> str:
        return self.version

    def get_release_date(self) -> datetime:
        return self.release_date