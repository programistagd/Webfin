from django.db import models
from django.utils import timezone
from django.conf import settings

# TODO for now categories are global, but it would be better to have private cats
class Category(models.Model):
    parent = models.ForeignKey('self', blank=True)
    name = models.CharField(max_length=30)


class Expense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.OneToOneField(settings.AUTH_USER_MODEL)
    kind = models.CharField(max_length=10)
    description = models.CharField(max_length=400)
    date = models.DateTimeField()
