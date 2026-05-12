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

