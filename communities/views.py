from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render

from .models import *


def home(request):
    memberships = []
    if request.user.is_authenticated():
        memberships = request.user.membership_set.all()
    ctx = {"memberships": memberships}
    return render(request, "Communities/home.html", ctx)


@login_required
def community_add(request):
    raise PermissionDenied()


@login_required
def community_view(request, cid):
    community = Community.objects.get(pk=cid)
    if request.user.membership_set.filter(community=community).count() <= 0:
        raise PermissionDenied()

    transactions = community.transaction_set.all()

    ctx = {
        "name": community.name,
        "about": community.about,
        "transactions": transactions,
        "owner": community.owner == request.user
    }
    return render(request, "Communities/community_view.html", ctx)