from dataclasses import dataclass

@dataclass
class Student:
    id: int
    name: str
    email: str
    password: str