from django import forms
from django.contrib.auth.models import User


class NormalTransactionForm(forms.Form):
    target = forms.ModelChoiceField(User.objects.all(), label="Receiver")
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    description = forms.CharField(max_length=140)


class ShopTransactionForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    description = forms.CharField(max_length=140)