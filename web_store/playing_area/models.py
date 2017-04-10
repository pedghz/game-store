from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    name = models.CharField(max_length=30, unique=True)
    # developer_id = models.ForeignKey(User, related_name='developer_id')
    url = models.URLField(max_length=150, unique=True)
    price = models.FloatField(default=0)
    image_url = models.URLField(max_length=150, default='')
    genre = models.CharField(max_length=2, default='ot')

    class Meta:
        ordering = ['name']


class GameState(models.Model):
    max_score = models.FloatField(default=0)
    gameState = models.CharField(max_length=1500)
    player_id = models.ForeignKey(User, related_name='user_id', on_delete=models.CASCADE)
    game_id = models.ForeignKey(Game, related_name='game_id', on_delete=models.CASCADE)

