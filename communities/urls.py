from django.conf.urls import url

from . import views

app_name = 'Communities'
urlpatterns = [
    url(r'^communities/add$', views.community_add, name='community_add'),
    url(r'^(?P<cid>[0-9]+)/$', views.community_view, name='community_view'),
    url(r'^$', views.home, name='home'),
]