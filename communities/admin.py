from django.contrib import admin

from .models import *

admin.site.register(Community)
admin.site.register(Membership)
admin.site.register(Transaction)