from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render

from .models import *


def home(request):
    all = Community.objects.all() # TODO not sure if will do it that way later
    ctx = {"communities": all}
    return render(request, "Communities/home.html", ctx)


@login_required
def community_add(request):
    raise PermissionDenied