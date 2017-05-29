from django.conf.urls import url, include
from . import views

app_name = 'authentication'

urlpatterns = [
    url(r'^$', views.login_register_page, name='login_register_page'),
    url(r'^login/$', views.login_view, name='my_login'),
    url(r'^logout/$', views.logout_view, name="my_logout"),
    url(r'^register/$', views.register_view, name="my_register"),
    url(r'^add_game/$', views.add_game, name="my_games"),
    url(r'^developer_games/$', views.developer_games, name='developer_games'),
    url(r'^my_profile/$', views.my_profile, name="my_profile"),
    url(r'^my_profile/reset_password/$', views.reset_password, name="my_reset_password"),

]
