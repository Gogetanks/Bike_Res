from enum import Enum

class ReservationStatus(Enum):
    PENDING = 'Pending'
    CONFIRMED = 'Confirmed'
    NOT_CONFIRMED = 'Not confirmed'
    FINISHED = 'Finished'

    @classmethod
    def choices(cls):
        return ((item.name, item.value) for item in cls)
