from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from kid.models import Kid

# Create your views here.

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)

            if user.is_staff:
                return redirect("teacher-dashboard")
            
            elif Kid.objects.filter(user=user).exists():
                return redirect("kid")

            elif hasattr(user, "student_profile"):
                return redirect("student-dashboard")

            else:
                messages.error(request, "No role assigned to this user")
                return redirect("login")

        messages.error(request, "Invalid credentials")

    return render(request, "account/login.html")


def logout(request):
    auth_logout(request)
    return redirect("landing")
