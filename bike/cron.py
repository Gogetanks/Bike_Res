from .enums import ComplaintStatus
from .models import Complaint
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
