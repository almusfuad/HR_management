from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Employee(models.Model):
      user = models.OneToOneField(User, on_delete=models.CASCADE)
      position = models.CharField(max_length=100)
      department = models.CharField(max_length=100)
      annual_leave = models.IntegerField(default=30, blank=True, null=True)
      
      def __str__(self):
            return self.user.username