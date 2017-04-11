from django.shortcuts import render
from django.http import HttpResponse
from .forms import shoppingCartForm
from playing_area.models import Game



def shopping_cart(request):
        # When requesting this page with GET, we simply return the cart status.
        # The cart status is mapped in the session variable cart_items, which is an array
        # that contains a list of IDs of games. Every time this page is requested,
        # the games data is update
        id=1
        game = Game.objects.all()
        game_ids = request.session.get('cart_items', [])
        return render(request, 'purchase/shopping_cart.html', {'cart': game })
