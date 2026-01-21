from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib import messages

# Create your views here.

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")

        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)

            # role-based redirect
            if user.is_staff:
                return redirect('teacher-dashboard')
            else:
                return redirect('student-dashboard')

        messages.error(request, "Invalid credentials")

    return render(request, "account/login.html")

def logout(request):
    auth.logout(request)
    return redirect("main")