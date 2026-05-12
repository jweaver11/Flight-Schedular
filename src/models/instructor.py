from dataclasses import dataclass

@dataclass
class Instructor:
    id: int
    name: str
    email: str
    password: str