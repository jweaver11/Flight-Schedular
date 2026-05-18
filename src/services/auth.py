"""
Authentication helpers.

  hash_password(raw)            → bcrypt hash to store in the DB
  verify_login(email, raw)      → dict with user info on success, None on failure

Security notes
--------------
* Passwords are hashed with bcrypt (cost factor 12) using the bcrypt library directly.
* verify_login always returns the same generic error regardless of whether the
  email or the password was wrong, so callers cannot enumerate valid addresses.
* The raw password is never logged, stored, or returned.
"""

from __future__ import annotations

import bcrypt

from services.db import admins_col, instructors_col, students_col

# bcrypt work factor – increase over time as hardware improves (12 is a safe minimum).
_BCRYPT_ROUNDS = 12


def hash_password(raw_password: str) -> str:
    """
    Hash a plaintext password for storage.
    Call this during registration, never at login time.
    """
    return bcrypt.hashpw(raw_password.encode(), bcrypt.gensalt(rounds=_BCRYPT_ROUNDS)).decode()


def _check_password(raw_password: str, stored_hash: str) -> bool:
    return bcrypt.checkpw(raw_password.encode(), stored_hash.encode())


def verify_login(email: str, raw_password: str) -> dict | None:
    """
    Look up *email* across all three collections (admins, instructors,
    students) and verify *raw_password* against the stored bcrypt hash.

    Returns a plain dict on success::

        {
            "email": "...",
            "name":  "...",
            "role":  "admin" | "instructor" | "student",
        }

    Returns None on failure (wrong email OR wrong password).
    The caller must not distinguish between the two failure reasons.
    """
    for collection, role in [
        (admins_col(),      "admin"),
        (instructors_col(), "instructor"),
        (students_col(),    "student"),
    ]:
        user = collection.find_one({"email": email.lower().strip()})
        if user:
            if _check_password(raw_password, user["password_hash"]):
                return {
                    "email": user["email"],
                    "name":  user.get("name", ""),
                    "role":  role,
                }
            # Email found but password wrong – return None immediately.
            # Don't tell the caller which one was wrong.
            return None

    # No document with that email in any collection.
    return None


class EmailAlreadyExistsError(Exception):
    """Raised when a registration is attempted with an email already in use."""


def register_student(email: str, raw_password: str, name: str = "", phone: str = "", ) -> dict:
    """
    Create a new student account in the Students collection.

    Parameters
    ----------
    email        : The student's email address (must be unique).
    raw_password : The plaintext password supplied by the user.
                   It is hashed immediately and the raw value is discarded.
    name         : Optional full name.
    phone        : Optional phone number.

    Returns
    -------
    A dict with the inserted document's details (without password_hash).

    Raises
    ------
    EmailAlreadyExistsError  : if that email is already registered.
    ValueError               : if email or password are blank.
    """
    email = email.lower().strip()

    if not email or not raw_password or not phone.strip():
        raise ValueError("Email, phone number, and password are required.")

    col = students_col()

    if col.find_one({"email": email}, {"_id": 1}):
        raise EmailAlreadyExistsError("An account with that email already exists.")

    doc = {
        "email":         email,
        "name":          name.strip(),
        "phone_number":  phone.strip(),
        "password_hash": hash_password(raw_password),
        "role":          "student",
    }

    col.insert_one(doc)

    # Return a safe summary — never return the hash.
    return {"email": email, "name": doc["name"], "role": "student"}


def reset_student_password(email: str, new_raw_password: str) -> bool:
    """
    Update the password_hash for a student account identified by email.

    Returns True if the student was found and updated, False if no matching
    student account exists.

    Raises
    ------
    ValueError : if email or new_raw_password is blank.
    """
    email = email.lower().strip()
    if not email or not new_raw_password:
        raise ValueError("Email and new password are required.")
    result = students_col().update_one(
        {"email": email},
        {"$set": {"password_hash": hash_password(new_raw_password)}},
    )
    return result.matched_count > 0


def register_instructor(email: str, raw_password: str, name: str = "") -> dict:
    """
    Create a new instructor account in the Instructors collection.

    Parameters
    ----------
    email        : The instructor's email address (must be unique).
    raw_password : The plaintext password supplied by the admin.
                   It is hashed immediately and the raw value is discarded.
    name         : Full name.
    schedule     : Optional schedule string (e.g. "Mon–Fri 9 am–5 pm").

    Returns
    -------
    A dict with the inserted document's details (without password_hash).

    Raises
    ------
    EmailAlreadyExistsError  : if that email is already registered.
    ValueError               : if email or password are blank.
    """
    email = email.lower().strip()

    if not email or not raw_password:
        raise ValueError("Email and password are required.")

    # Check across all collections so an email can't be reused in another role.
    for col in (admins_col(), instructors_col(), students_col()):
        if col.find_one({"email": email}, {"_id": 1}):
            raise EmailAlreadyExistsError("An account with that email already exists.")

    doc = {
        "email":         email,
        "name":          name.strip(),
        "schedule":      {
            'Sunday':    "",
            'Monday':    "9:00-17:00",
            'Tuesday':   "9:00-17:00",
            'Wednesday': "9:00-17:00",
            'Thursday':  "9:00-17:00",
            'Friday':    "9:00-17:00",
            'Saturday':  "",
        },
        "password_hash": hash_password(raw_password),
        "role":          "instructor",
    }

    instructors_col().insert_one(doc)

    # Return a safe summary — never return the hash.
    return {"email": email, "name": doc["name"], "role": "instructor"}
