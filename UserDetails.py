from dataclasses import dataclass 
@dataclass
class UserDetails:
    username: str
    email: str
    
    def __init__(self):
        if self.id is None:
            self.id = 0
        else:
            self.id = self.id + 1
        
        self.email = self.email.lower()

    def set_email(self, email: str) -> None:
        self.email = email.lower()

    def set_username(self, username: str) -> None:
        self.username = username

    def get_username(self) -> str:
        return self.username

    def get_email(self) -> str:
        return self.email

