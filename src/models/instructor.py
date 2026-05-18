from dataclasses import dataclass


@dataclass
class Instructor:
    email: str          # Key / unique index in DB
    name: str
    phone_number: str
    password_hash: str  # bcrypt hash — never store the raw password
    schedule: list      # Standard weekly schedule for the instructor\
            # [{'Monday': (0900, 1700)}, {'Tuesday': (0900, 1700)}...]
    role: str = "instructor"