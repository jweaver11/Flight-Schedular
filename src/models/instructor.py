from dataclasses import dataclass


@dataclass
class Instructor:
    email: str          # Key / unique index in DB
    name: str
    password_hash: str  # bcrypt hash — never store the raw password
    schedule: list      # Standard weekly schedule for the instructor
    role: str = "instructor"