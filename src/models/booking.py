from dataclasses import dataclass

@dataclass
class Booking:
    id: int
    date: str           # Date of the booking
    time: str           # Time of start of the booking
    duration: int       # Duration of the booking in minutes
    students: list        # Student ID for the booking
    instructors: list      # Instructor ID for the booking
    aircrafts: list        # Aircraft ID for the booking
    equipment: list       # List of equipment IDs for the booking
    type: str           # Type of booking (lesson, checkride, etc)    

    cancelled: bool = False                  # Determines if this booking was cancelled. It won't be deleted
    instructor_time_off: bool = False        # Determines if this booking is a day off for an instructor - meaning they can't be booked
    aircraft_maintenance: bool = False       # Determines if this booking is for aircraft maintenance - meaning it can't be booked
