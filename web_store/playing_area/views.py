# from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import JsonResponse
# from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from playing_area.models import GameState
from playing_area.models import Game
from django.contrib.auth.models import User
from django.shortcuts import redirect



def my_index(request):
    context= {}
    games_list = Game.objects.all()
    context['counter']=1
    context['games_list'] = games_list
    context['user_is_authenticated'] = request.user.is_authenticated()
    return render(request, "playing_area/index.html", context)


def my_gameslist(request):
    context = {}
    context['user_is_authenticated'] = request.user.is_authenticated()
    return HttpResponse("the GAMESLIST view is not ready yet")


def playing_game(request):
    game_name = request.path.split('/')[2]
    game = Game.objects.get(name=game_name)
    try:
        user = User.objects.get(user_id=request.user.id)
    except User.DoesNotExist:
        return redirect('/accounts/')
    source = game.url

    context = {}

    if request.is_ajax():

        if request.POST.get('messageType', None) == 'SCORE':
            score = request.POST.get('score', None)
            score = float(score)
            result = {}
            game_state_objects = GameState.objects.filter(game_id__id = game.id, player_id__id = request.user.id)

            if game_state_objects.count() == 0:
                obj = GameState(max_score=score, player_id=user, game_id=game)
                obj.save()
                result['result'] = 'saved'
            else:
                for G_S_OBEJCT in game_state_objects:
                    max_score = G_S_OBEJCT.max_score
                    if max_score < score:
                        G_S_OBEJCT.max_score = score
                        G_S_OBEJCT.player_id=user
                        G_S_OBEJCT.game_id=game
                        G_S_OBEJCT.save()
                        result['result'] = 'updated'
                    else:
                        result['result'] = 'not updated'

            result['error'] = False
            return JsonResponse({'result': result})

        elif request.POST.get('messageType', None) == 'LOAD_REQUEST':
            game_state_objects = GameState.objects.filter(game_id__id = game.id, player_id__id = request.user.id)
            for G_S_OBEJCT in game_state_objects:
                # gameState = game.gameState
                data = {'messageType': 'LOAD',
                    'gameState': G_S_OBEJCT.gameState,
                    }
                return JsonResponse(data)

        elif request.POST.get('messageType', None) == 'SAVE':
            score = float(request.POST.get('score', None))
            game_state = str(request.POST.get('gameState', None))
            result = {}
            game_state_objects = GameState.objects.filter(game_id__id = game.id, player_id__id = request.user.id)

            if game_state_objects.count() == 0:
                obj = GameState(max_score=score, game_state=game_state, player_id=user, game_id=game)
                obj.save()
                result['result'] = 'first try saved'
            else:
                for G_S_OBEJCT in game_state_objects:
                    G_S_OBEJCT.gameState = game_state
                    G_S_OBEJCT.player_id = user
                    G_S_OBEJCT.game_id = game
                    G_S_OBEJCT.save()
                    result['result'] = score

            result['error'] = False
            return JsonResponse({'result': result})

    if source.endswith('/'):
        source = source[:-1]

    context['source'] = source
    context['user_is_authenticated'] = request.user.is_authenticated()
    return render(request, "playing_area/playgame.html", context)