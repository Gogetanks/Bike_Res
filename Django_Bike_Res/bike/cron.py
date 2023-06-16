from .enums import ComplaintStatus
from .models import Complaint, Reservation, Bike
from datetime import datetime

def close_complaints():
    complaints = Complaint.objects.filter(status='SOLVED')
    now = datetime.now()
    for complaint in complaints:
        # After 5 days of being SOLVED, we close the complaint
        if (now - complaint.lastUpdate).days >= 5:
            complaint.status = ComplaintStatus.CLOSED.name
            complaint.save()

def remove_complaints():
    complaints = Complaint.objects.filter(status='CLOSED')
    now = datetime.now()
    for complaint in complaints:
        # After 1 year of being CLOSED, we delete the complaint
        if (now - complaint.lastUpdate).days >= 365:
            complaint.delete()

def close_reservation():
    reservations = Reservation.objects.filter(status='FINISHED')
    now = datetime.now()
    for reservation in reservations:
        bike = Bike.objects.get(id=reservation.bike.id)
        # 1 day after the endDate, we set the bike in_stock
        if (now - reservation.endDate).days >= 1:
            bike.in_stock = True