from rest_framework import generics, permissions
from .permissions import IsOwner
from .serializers import GameJsonSerializer
from playing_area.models import Game
from authentication.models import Profile

class CreateView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    serializer_class = GameJsonSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
        serializer.save(developer=self.request.user)

    def get_queryset(self):
        developer = Profile.objects.get(user_id=self.request.user.id)
        queryset = Game.objects.filter(developer=developer)
        return queryset



#RetrieveUpdateDestroyAPIView is a generic view that provides GET(one), PUT, PATCH and DELETE method handlers.
class DetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""

    serializer_class = GameJsonSerializer
    permission_classes = (permissions.IsAuthenticated,IsOwner)

    def get_queryset(self):
        developer = Profile.objects.get(user_id=self.request.user.id)
        queryset = Game.objects.filter(developer=developer)
        return queryset