from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from . forms import LoginForm
from django.contrib import messages

# Create your views here.
def user_login(request):
      if request.method == "POST":
            form = LoginForm(request, request.POST)
            
            if form.is_valid():
                  username = form.cleaned_data['username']
                  password = form.cleaned_data['password']
                  user = authenticate(request, username=username, password=password)
                  if user is not None:
                        login(request, user)
                        messages.success(request, 'Login successful.')
                        return redirect('login')
                  else:
                        messages.error(request, 'Invalid username or password.')
                        return redirect('login')
      else:
            form = LoginForm()
      return render(request, 'core/login.html', {'form': form})


def user_logout(request):
      if request.method == 'GET':
            logout(request)
            messages.error(request, 'Logout successful.')
            return redirect('login')