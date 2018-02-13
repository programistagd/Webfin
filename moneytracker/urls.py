from django.conf.urls import url
from django.views.generic import RedirectView

from . import views

app_name = 'MoneyTracker'
urlpatterns = [
    url(r'^import$', views.import_expenses, name='import_expenses'),
    url(r'^$', views.show_expenses, name='show_expenses'),
    url(r'^home$', RedirectView.as_view(pattern_name='MoneyTracker:show_expenses', permanent=False), name="home")
]