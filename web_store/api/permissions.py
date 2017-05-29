from rest_framework.permissions import BasePermission ,SAFE_METHODS
from playing_area.models import Game
from authentication.models import Profile


class IsOwner(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if isinstance(obj,Game):
            return request.user and obj.developer.user_id == request.user.id
        return False


