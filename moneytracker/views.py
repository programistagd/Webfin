from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import *

@login_required
def import_expenses(request):
    return render(request, "MoneyTracker/import_start.html", {})

@login_required
def show_expenses(request):
    return render(request, "MoneyTracker/show.html", {})