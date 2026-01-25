from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from kid.models import Kid

# Create your views here.

@login_required
def kid(request):
    return render(request, "kid/kid.html")
