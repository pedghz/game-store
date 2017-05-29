from rest_framework import serializers
from playing_area.models import Game,GameState



class GameStateSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    class Meta:
        model = GameState
        fields = ('max_score',)

class GameJsonSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    gameid = GameStateSerializer(many=True)

    developer = serializers.ReadOnlyField(source='developer.id')

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Game
        fields = ('id', 'name', 'developer', 'url', 'price','genre', 'purchased_times', 'date_time', 'gameid')

