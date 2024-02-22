import random
import string
import secrets

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from employee.models import Employee



POSITION_CHOICES = (
            ('N/A', '--------------------------------'),
            ('manager', 'Manager'),
            ('developer', 'Developer'),
            ('designer', 'Designer'),
            ('analyst', 'Analyst'),   
      )
      
DEPARTMENT_CHOICES = (
            ('N/A', '--------------------------------'),
            ('hr', 'Human Resources'),
            ('it', 'Information Technology'),
            ('finance', 'Finance'),
            ('marketing', 'Marketing'),
            ('operations', 'Operations'),
      )

class AddEmployeeForm(forms.ModelForm):
      first_name = forms.CharField(label='First Name', max_length=100)
      last_name = forms.CharField(label='Last Name', max_length=100)
      email = forms.EmailField(label='Email')
      position = forms.ChoiceField(label='Position', choices=POSITION_CHOICES)
      department = forms.ChoiceField(label='Department', choices=DEPARTMENT_CHOICES)
      
      class Meta:
            model = Employee
            fields =['first_name', 'last_name', 'email', 'position', 'department']
            
      def clean(self):
            cleaned_data = super().clean()
            password = self.generate_password()
            cleaned_data['password'] = password
            return cleaned_data
            
      def save(self, commit = True):
            cleaned_data = self.cleaned_data
            email = cleaned_data['email']
            password = self.generate_password()
            username = self.generate_username()
            
            
            # sending email
            email_subject = 'Welcome to the company'
            email_body = render_to_string('staff/emails/email_with_username_password.html', {
                  'username': self.generate_username(), 'password': password,
            })
            try:
                  email_message = EmailMultiAlternatives(email_subject, email_body, to=[email])
                  email_message.attach_alternative(email_body, 'text/html')
                  email_message.send()
            except BadHeaderError:
                  raise forms.ValidationError('Invalid email subject or body.')
            except Exception as e:
                  raise forms.ValidationError(f"Failed to send email to {email}. Please check the email address.")
            
            if commit:
                  user = User.objects.create_user(
                        username = username,
                        email = email,
                        password = password, 
                        first_name = self.cleaned_data['first_name'],
                        last_name = self.cleaned_data['last_name'],
                  )
                  
                  employee = Employee.objects.create(
                        user = user,
                        position = self.cleaned_data['position'],
                        department= self.cleaned_data['department']
                  )
                  return employee
            else:
                  return None
      
      
      def generate_username(self):
            first_name = self.cleaned_data['first_name']
            
            if ' ' in first_name:
                  _, last_name = first_name.split(' ', 1)
            else:
                  last_name = first_name
                  
            username = f"{last_name.lower()}.{self.cleaned_data['last_name'].lower()}"
            suffix = 1
            while User.objects.filter(username = username).exists():
                  username = f"{username}{suffix}"
                  suffix += 1
            return username
      
      
      def generate_password(self):
            uppercase_letters = string.ascii_uppercase
            lowercase_letters = string.ascii_lowercase
            digits = string.digits
            special_char = "!#%@&"
            
            # ensure at least one character form each category
            password = (
                  secrets.choice(uppercase_letters) +
                  secrets.choice(lowercase_letters) +
                  secrets.choice(digits) +
                  secrets.choice(special_char)
            )
      
            # add random character to the password
            password += ''.join(secrets.choice(
                  uppercase_letters + lowercase_letters + digits + special_char
            ) for _ in range(4))
            
            # shuffle the password to randomize the character order
            password_list = list(password)
            random.shuffle(password_list)
            password = ''.join(password_list)
            
            return password