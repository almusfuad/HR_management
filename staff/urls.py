from django.urls import path
from . import views

urlpatterns = [
      path('add_employee/', views.add_employee, name = 'add_employee'),
]