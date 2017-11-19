from django.db import models
from django.utils import timezone
from django.conf import settings


class Community(models.Model):
    name = models.CharField(max_length=32, unique=True, db_index=True)
    about = models.CharField(max_length=140)
    owner = models.OneToOneField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return str(self.name)


class Transaction(models.Model):
    concerning = models.ForeignKey(Community, db_index=True)
    who = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="outgoing_transactions")
    target = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name="incoming_transactions")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=140)
    deleted = models.BooleanField(default=False)
    date = models.DateTimeField()
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "$" + str(self.amount) + " - " + str(self.description)


class Membership(models.Model):
    community = models.ForeignKey(Community)
    user = settings.AUTH_USER_MODEL