from django.db import models
from django.contrib.auth.models import User




class Profile(models.Model):
    # We have two types of profiles: Developer and regular user.
    DEVELOPER = 'DEV'
    NORMAL_USER = 'USR'
    profile_type_enum = (
        (DEVELOPER, 'Developer'),
        (NORMAL_USER, 'Normal user')
    )

    # We create a foreign key to user.
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    # A user can either be a Developer or normal user.
    profile_type = models.CharField(
        max_length=3,
        choices=profile_type_enum,
        default=NORMAL_USER
    )

    ownedGames = models.ManyToManyField('playing_area.Game', default=None, blank=True)