from dataclasses import dataclass

@dataclass
class Booking:
    id: int
    date: str
    time: str
    students: int         # Student ID for the booking
    instructors: int      # Instructor ID for the booking
    aircrafts: int        # Aircraft ID for the booking
    type: str           # Type of booking (lesson, checkride, etc)

    

    cancelled: bool = False                 # Determines if this booking was cancelled. It won't be deleted
    instructor_time_off: bool = False       # Determines if this booking is a day off for an instructor - meaning they can't be booked
    aircraft_maintenance: bool = False       # Determines if this booking is for aircraft maintenance - meaning it can't be booked


# App data stored as events:
# bookings 
# Instructors
# Aircrafts
# Equipment
# Students
# Pricing
