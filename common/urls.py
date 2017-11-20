from django.conf.urls import url
from django.contrib.auth import views as auth_views


from . import views

app_name = 'common'
urlpatterns = [
    url(r'^accounts/signup/$', views.signup, name='signup'),
    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^accounts/logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
]