from enum import Enum

class ReservationStatus(Enum):
    PENDING = 'Pending'
    CONFIRMED = 'Confirmed'
    NOT_CONFIRMED = 'Not confirmed'
    FINISHED = 'Finished'

    @classmethod
    def choices(cls):
        return ((item.name, item.value) for item in cls)

class ComplaintStatus(Enum):
    UNATTACHED = 'Unattached'
    OPENED = 'Opened'
    SOLVED = 'Solved'
    CLOSED = 'Closed'

    @classmethod
    def choices(cls):
        return ((item.name, item.value) for item in cls)
