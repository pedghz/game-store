from django.conf.urls import url
from . import views

app_name = 'authentication'

urlpatterns = [
    url(r'^$', views.login_register_page, name='login_register_page'),
    url(r'^login/$', views.login_view, name='my_login'),
    url(r'^logout/$', views.logout_view, name="my_logout"),
    url(r'^register/$', views.register_view, name="my_register"),
    url(r'^add_game/$', views.add_game, name="my_games"),
]
