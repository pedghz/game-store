from django.db import models
from django.contrib.auth.models import User
# from django.core.urlresolvers import reverse
from datetime import datetime
from authentication.models import Profile


class Game(models.Model):
    name = models.CharField(max_length=30, unique=True)
    # developer_id = models.ForeignKey(User, related_name='developer_id')
    url = models.URLField(max_length=150)
    price = models.FloatField(default=0)
    image_url = models.URLField(max_length=150, default='')
    genre = models.CharField(max_length=15, default='Other')
    date_time = models.DateTimeField(default=datetime.now, blank=True)
    developer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    purchased_times = models.IntegerField(default=0)
    class Meta:
        ordering = ['name']

    def add_to_json(self, user=None):
        result = {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'price': self.price,
            'image_url': self.image_url,
            'genre':self.genre,
            'developer': self.developer,
            'purchased_times':self.purchased_times,
        }


        if user is not None and isinstance(user, User) and user.is_authenticated():
            bought_before = user.profile.ownedGames.filter(id=self.id)
            if bought_before.count() > 0:
                result['owned'] = True
            else:
                result['owned'] = False

        return result

class GameState(models.Model):
    max_score = models.FloatField(default=0)
    gameState = models.CharField(max_length=1500, default='')
    player_id = models.ForeignKey(User, related_name='user_id', on_delete=models.CASCADE)
    game_id = models.ForeignKey(Game, related_name='gameid', on_delete=models.CASCADE)
