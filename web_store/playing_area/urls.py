from django.conf.urls import url
from . import views

app_name = 'playing_area'

urlpatterns=[
    # our homepage
    url(r'^$', views.my_index, name='index'),
    # link to list of games
    url(r'^gameslist/$', views.my_gameslist, name='gameslist'),
    # links to games filtered by their genre
    url(r'^gameslist/[a-zA-Z0-9]+\S*/$', views.my_gameslist, name='gameslist'),
    # link to play a game
    url(r'^playgame/[a-zA-Z0-9]+\S*/$', views.playing_game, name='playgame'),
]