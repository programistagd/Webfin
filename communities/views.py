from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models.functions import Coalesce
from django.shortcuts import render, redirect
from django.db.models import Sum

from .forms import NormalTransactionForm, ShopTransactionForm
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


class ResultOverrideException(Exception):
    def __init__(self, result):
        self.result = result


@login_required
def community_view(request, cid):
    community = Community.objects.get(pk=cid)
    if request.user.membership_set.filter(community=community).count() <= 0:
        raise PermissionDenied()

    members = User.objects.filter(pk__in=community.membership_set.all())
    member_count = members.count()

    try:
        normal_form = handle_form_tx_add_normal(request, community, members)
        shop_form = handle_form_tx_add_shop(request, community)
    except ResultOverrideException as e:
        return e.result

    transactions = community.transaction_set.order_by('-date').all()
    txs = community.transaction_set.filter(deleted=False)

    shop_txs = txs.filter(target__isnull=True)
    sum_of_costs = shop_txs.aggregate(sum=Coalesce(Sum("amount"), 0))["sum"]
    cost_per_person = sum_of_costs / member_count

    balances = []
    for user in members:
        b = 0
        b += txs.filter(who=user).aggregate(sum=Coalesce(Sum("amount"), 0))["sum"]
        b -= txs.filter(target=user).aggregate(sum=Coalesce(Sum("amount"), 0))["sum"]
        b -= cost_per_person
        balances.append({"name": user, "balance": b})

    ctx = {
        "cid": cid,
        "name": community.name,
        "about": community.about,
        "transactions": transactions,
        "owner": community.owner == request.user,
        "balances": balances,
        "normal_form": normal_form,
        "shop_form": shop_form,
    }

    return render(request, "Communities/community_view.html", ctx)


def handle_form_tx_add_normal(request, community, members):
    if request.method == "POST" and request.POST.get("form_type", "") == "normal":
        form = NormalTransactionForm(request.POST)
        if form.is_valid():
            tx = Transaction()
            tx.concerning = community
            tx.who = request.user
            tx.target = form.cleaned_data["target"]
            tx.amount = form.cleaned_data["amount"]
            tx.description = form.cleaned_data["description"]
            tx.date = timezone.now()
            tx.save()
            messages.success(request, "Added transaction")
            raise ResultOverrideException(redirect("Communities:community_view", cid=community.pk))
        return form

    form = NormalTransactionForm()
    form.fields["target"].queryset = members.exclude(id=request.user.id)
    return form


def handle_form_tx_add_shop(request, community):
    if request.method == "POST" and request.POST.get("form_type", "") == "shop":
        form = ShopTransactionForm(request.POST)
        if form.is_valid():
            tx = Transaction()
            tx.concerning = community
            tx.who = request.user
            tx.target = None
            tx.amount = form.cleaned_data["amount"]
            if tx.amount < 0:
                messages.warning(request, "Cannot purchase an item with negative price.")
                return form
            tx.description = form.cleaned_data["description"]
            tx.date = timezone.now()
            tx.save()
            messages.success(request, "Added purchase")
            raise ResultOverrideException(redirect("Communities:community_view", cid=community.pk))
        return form

    return ShopTransactionForm()
