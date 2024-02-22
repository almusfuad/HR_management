from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta

# Create your models here.
class Employee(models.Model):
      user = models.OneToOneField(User, on_delete=models.CASCADE)
      position = models.CharField(max_length=100)
      department = models.CharField(max_length=100)
      annual_leave = models.IntegerField(default=30, blank=True, null=True)
      
      def __str__(self):
            return self.user.username
      
      
class AttendanceRecord(models.Model):
      employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
      date = models.DateField()
      check_in_time = models.TimeField()
      check_out_time = models.TimeField(null=True, blank = True)
      
      def __str__(self):
            return f'{self.employee.user.username}   -   {self.date}  -  {self.get_duration()}'
      
      def get_duration(self):
            if self.check_out_time and self.check_in_time:
                  check_in_datetime = datetime.combine(self.date, self.check_in_time)
                  check_out_datetime = datetime.combine(self.date, self.check_out_time)
                  
                  # calculate duration
                  duration = check_out_datetime - check_in_datetime
                  hours = duration.total_seconds() / 3600
                  return round(hours, 2)
            else:
                  return None


      
class LeaveRequest(models.Model):
      STATUS_CHOICES = (
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
      )
      
      employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
      leave_type = models.CharField(max_length=50)
      start_date = models.DateField()
      end_date = models.DateField()
      status = models.CharField(max_length=20, choices=STATUS_CHOICES, default = 'pending')
      
      def __str__(self):
            return f'{self.employee.user.username}   -   {self.leave_type}'