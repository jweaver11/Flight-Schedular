from dataclasses import dataclass


@dataclass
class Student:
    email: str          # Key / unique index in DB
    name: str
    password_hash: str  # bcrypt hash — never store the raw password
    phone_number: str
    role: str = "student"