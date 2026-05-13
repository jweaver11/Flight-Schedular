"""
MongoDB connection singleton.

Reads MONGO_URI and DB_NAME from the .env file (via python-dotenv).
The connection is created once and reused across the application.
"""

import os
from functools import lru_cache

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.database import Database

load_dotenv()


@lru_cache(maxsize=1)
def get_db() -> Database:
    """
    Return the application database.  The MongoClient (and its connection
    pool) is created exactly once per process thanks to @lru_cache.
    """
    uri = os.environ.get("MONGO_URI")
    db_name = os.environ.get("DB_NAME", "Chopper_Aviation_Database")

    if not uri:
        raise RuntimeError(
            "MONGO_URI is not set.  "
            "Create a .env file with MONGO_URI=<your connection string>."
        )

    client = MongoClient(uri)
    return client[db_name]


# Convenience accessors so callers never hard-code collection names.
def admins_col():
    return get_db()["admins"]

def instructors_col():
    return get_db()["instructors"]

def students_col():
    return get_db()["students"]

def bookings_col():
    return get_db()["bookings"]

def pricing_col():
    return get_db()["pricing"]

def aircrafts_col():
    return get_db()["aircraft"]

def equipment_col():
    return get_db()["equipment"]


# ── Delete helpers ────────────────────────────────────────────────────────────

def delete_student(name: str, email: str) -> bool:
    """Delete a student matched by both name and email. Returns True if deleted."""
    result = students_col().delete_one({"name": name, "email": email})
    return result.deleted_count > 0

def delete_instructor(name: str, email: str) -> bool:
    """Delete an instructor matched by both name and email. Returns True if deleted."""
    result = instructors_col().delete_one({"name": name, "email": email})
    return result.deleted_count > 0

def delete_aircraft(name: str) -> bool:
    """Delete an aircraft matched by name/tail number. Returns True if deleted."""
    result = aircrafts_col().delete_one({"name": name})
    return result.deleted_count > 0

def delete_equipment(name: str) -> bool:
    """Delete an equipment item matched by name. Returns True if deleted."""
    result = equipment_col().delete_one({"name": name})
    return result.deleted_count > 0

def delete_pricing(name: str) -> bool:
    """Delete a pricing entry matched by service name. Returns True if deleted."""
    result = pricing_col().delete_one({"name": name})
    return result.deleted_count > 0

def cancel_booking(booking_id: str) -> bool:
    """Mark a booking as cancelled (does not delete it). Returns True if updated."""
    from bson import ObjectId
    result = bookings_col().update_one(
        {"_id": ObjectId(booking_id)},
        {"$set": {"cancelled": True}},
    )
    return result.modified_count > 0


def add_aircraft(name: str, aircraft_type: str, capacity: int, weight_limit: float = 0.0) -> bool:
    """Insert a new aircraft. Returns False if a record with that name already exists."""
    if aircrafts_col().find_one({"name": name}, {"_id": 1}):
        return False
    aircrafts_col().insert_one({"name": name, "type": aircraft_type, "capacity": capacity, "weight_limit": weight_limit})
    return True


def add_equipment(name: str, count: int) -> None:
    """Add equipment, incrementing count if the item already exists (upsert)."""
    equipment_col().update_one({"name": name}, {"$inc": {"count": count}}, upsert=True)


def add_pricing(name: str, cost: float) -> bool:
    """Insert a new pricing entry. Returns False if that service name already exists."""
    if pricing_col().find_one({"name": name}, {"_id": 1}):
        return False
    pricing_col().insert_one({"name": name, "cost": cost})
    return True

def add_booking(
    date: str,
    time: str,
    duration: int,
    students: list,
    instructors: list,
    aircrafts: list,
    equipment: list = None,
    type: str = "lesson",
    instructor_time_off: bool = False,
    aircraft_maintenance: bool = False,
) -> str:
    """Insert a new booking. Returns the inserted document's ID as a string."""
    # Check for scheduling conflicts: same date/time with any overlapping instructor or aircraft
    existing = bookings_col().find_one({
        "date": date,
        "time": time,
        "cancelled": {"$ne": True},
        "$or": [
            {"instructors": {"$in": instructors}},
            {"aircrafts":   {"$in": aircrafts}},
        ],
    })
    if existing:
        raise ValueError("One or more instructors or aircraft are already booked at that date and time.")
    result = bookings_col().insert_one({
        "date": date,
        "time": time,
        "duration": duration,
        "students": students,
        "instructors": instructors,
        "aircrafts": aircrafts,
        "equipment": equipment or [],
        "type": type,
        "cancelled": False,
        "instructor_time_off": instructor_time_off,
        "aircraft_maintenance": aircraft_maintenance,
    })
    return str(result.inserted_id)

