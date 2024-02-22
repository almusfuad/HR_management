from django.shortcuts import render, redirect
from .forms import AddEmployeeForm


from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

def add_employee(request):
      if request.method == 'POST':
            form = AddEmployeeForm(request.POST)
            if form.is_valid():
                  employee = form.save()
                  return redirect('add_employee')
      else:
            form = AddEmployeeForm()
      return render(request, 'staff/add_employee.html', {'form': form})