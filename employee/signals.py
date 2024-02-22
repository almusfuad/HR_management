from . import models
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.utils import timezone
import logging

# get logger instance
logger = logging.getLogger(__name__)

# Create your views here.
@receiver(user_logged_in)
def attendance_start(sender, request, user, **kwargs):
      employee = models.Employee.objects.get(user = user)
      print(employee)
      today = timezone.now().date()
      attendance, created = models.AttendanceRecord.objects.get_or_create(
            employee=employee, date=today,
            defaults={'check_in_time': timezone.now().time()}
      )
      if not created:
            # Update the check-in time if the record already exists
            attendance.check_in_time = timezone.now().time()
            attendance.save()
      
@receiver(user_logged_out)
def attendance_finish(sender, request, user, **kwargs):
      employee = models.Employee.objects.get(user = user)
      today = timezone.now().date()
      attendance = models.AttendanceRecord.objects.get(employee = employee, date = today)
      attendance.check_out_time = timezone.now().time()
      attendance.save()
      
      
# connect signal to function
user_logged_in.connect(attendance_start)
user_logged_out.connect(attendance_finish)