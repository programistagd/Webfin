from django.conf.urls import url

from . import views

app_name = 'Communities'
urlpatterns = [
    url(r'^communities/add$', views.community_add, name='community_add'),
    url(r'^$', views.home, name='home'),
]