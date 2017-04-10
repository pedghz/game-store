from django.conf.urls import url
from . import views

app_name = 'playing_area'

urlpatterns=[
    url(r'^$', views.my_index, name='index'),
    url(r'^gameslist/$', views.my_gameslist, name='gameslist'),
    url(r'^playgame/[a-zA-Z0-9]+\S*/$', views.playing_game, name='playgame'),

]