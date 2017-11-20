from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models.functions import Coalesce
from django.shortcuts import render
from django.db.models import Sum

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
    txs = community.transaction_set.filter(deleted=False)

    members = community.membership_set.all()
    member_count = len(members)

    shop_txs = txs.filter(target__isnull=True)
    sum_of_costs = shop_txs.aggregate(sum=Coalesce(Sum("amount"), 0))["sum"]
    cost_per_person = sum_of_costs / member_count

    balances = []
    for m in members:
        user = m.user
        b = 0
        b += txs.filter(who=user).aggregate(sum=Coalesce(Sum("amount"), 0))["sum"]
        b -= txs.filter(target=user).aggregate(sum=Coalesce(Sum("amount"), 0))["sum"]
        b -= cost_per_person
        balances.append({"name": user, "balance": b})

    ctx = {
        "name": community.name,
        "about": community.about,
        "transactions": transactions,
        "owner": community.owner == request.user,
        "balances": balances,
    }
    return render(request, "Communities/community_view.html", ctx)