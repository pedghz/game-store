from django.db import models
from django.utils.timezone import now
from playing_area.models import Game
from django.contrib.auth.models import User
from authentication.models import Profile
from datetime import datetime



def get_default_ymd():
    return now().date().strftime("%Y%m%d")

class Order(models.Model):
    id=models.AutoField(primary_key=True)
    _player = models.ForeignKey(Profile, null=False)
    _games = models.ManyToManyField(Game, default=None, blank=True)
    total = models.FloatField(default=0, null=False)

    orderDate = models.DateTimeField(default=datetime.now, null=False)
    orderDateYearMonthDay = models.CharField(max_length=8, default=get_default_ymd, null=False)

    paymentDate = models.DateTimeField(default=datetime.now, null=True)
    paymentRef = models.IntegerField(null=True, default=0)
    status = models.CharField(max_length=10, null=False, default="pending")

    def __str__(self):
        return str(self.total)