from dataclasses import dataclass
from typing import List
from datetime import datetime

@dataclass
class Driver:
    name: str
    version: str
    release_date: datetime
    install_command: str
    package_size: float
    device_class: str
    

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

    def get_install_command(self) -> str:
        return self.install_command

    def get_package_size(self) -> float:
        return self.package_size

    def get_device_class(self) -> str:
        return self.device_class