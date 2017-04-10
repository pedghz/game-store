# from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import JsonResponse
# from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from playing_area.models import GameState
from playing_area.models import Game
from django.contrib.auth.models import User


def my_index(request):
    context= {}
    games_list = Game.objects.all()
    context['games_list'] = games_list
    return render(request, "playing_area/index.html", context)


def my_gameslist(request):
    return HttpResponse("the GAMESLIST view is not ready yet")


def playing_game(request):
    game_name = request.path.split('/')[2]
    game = Game.objects.get(name=game_name)
    source = game.url

    context = {}

    if request.is_ajax():
        if (request.POST.get('messageType', None) == 'SCORE'):
            request_data = request.POST.get('score', None)
            return JsonResponse({'score': request_data})
        elif (request.POST.get('messageType', None) == 'LOAD_REQUEST'):
            gameState = {
                        'playerPos': {
                            "x": 300,
                            "y": 300
                        },
                        'ghost1': {
                            "x": 0,
                            "y": 0
                        },
                        'ghost2': {
                            "x": 512,
                            "y": 480
                        },
                        'ghost3': {
                            "x": 512,
                            "y": 0
                        },
                        'ghost4': {
                            "x": 0,
                            "y": 480
                        },
                        'diamond': {
                            "x": 200,
                            "y": 200
                        },
                        'score': 10,
                    }
            data = {'messageType': 'LOAD',
                    'gameState': gameState,
                    }
            return JsonResponse({'result': gameState})
            # context = {'source': request.get_full_path().split("/")[2] }

    if source.endswith('/'):
        source = source[:-1]

    context['source'] = source
    return render(request, "playing_area/playgame.html", context)