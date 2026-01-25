from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def kid_list(request):
    if not request.user.is_staff:
        return redirect("kid")