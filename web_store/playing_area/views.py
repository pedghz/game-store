# from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import JsonResponse
# from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404
from playing_area.models import GameState
from playing_area.models import Game
from django.contrib.auth.models import User
from django.shortcuts import redirect
from authentication.forms import AddGame
from playing_area.forms import SearchGame, GameStateForm, GameScoreForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from authentication.models import Profile
from purchase.views import add_to_cart
from django import forms


def my_index(request):
    context= {}
    # if request.user.is_authenticated():
    #     try:
    #         user_type = Profile.objects.get(user_id=request.user.id).profile_type
    #     except User.DoesNotExist:
    #         return redirect('/accounts/')
        # if user_type == 'DEV':
        #     context['dev'] = 'True'
            # return redirect('/accounts/my_profile/', context)
    # context= {}
    games_list = Game.objects.all().order_by('-date_time')[:4]
    context['counter']=1
    context['games_list'] = games_list

    return render(request, "playing_area/index.html", context)


def my_gameslist(request):
    context = {'search_game': SearchGame(request.POST)}
    if request.user.is_authenticated():
        try:
            user_type = Profile.objects.get(user_id=request.user.id).profile_type
        except User.DoesNotExist:
            return redirect('/accounts/')
        # if user_type == 'DEV':
        #     context['dev'] = 'True'
            # return redirect('/accounts/my_profile/')
    context['counter'] = 1
    genre_list = []
    for genre in AddGame.genre_choices:
        genre_list.append(genre[0])
    context['genres'] = genre_list
    if request.method == "POST":
        form = SearchGame(request.POST)
        if form.is_valid():
            keyword = form.cleaned_data["keyword"]
            keyword = keyword.lower().replace(' ', '-')
            games_list = Game.objects.filter(name__icontains=keyword)
            context['games_list'] = games_list
        else:
            context['error_search'] = 'True'
            context['error_message'] = 'The form is not valid!'
    else:
        games_list = Game.objects.all()
        context['games_list'] = games_list
        if request.is_ajax() and request.path.split('/')[2] != '':
            games_list = Game.objects.filter(genre=request.path.split('/')[2])
            if games_list.count() > 0:
                context['games_list'] = games_list
            else:
                context['games_list'] = {}
            if request.POST.get('messageType', None) != None:
                genre = request.POST.get('messageType', None)
                games_list = Game.objects.filter(genre=genre)
                if games_list.count() > 0:
                    context['games_list'] = games_list
                else:
                    context['games_list'] = {}
                return render(request, "playing_area/gameslist_genre.html", context)
        if (request.path.split('/')[2] != ''):
            return render(request, "playing_area/gameslist.html", context)

    return render(request, "playing_area/gameslist.html", context)


@login_required
def playing_game(request):
    context = {}
    game_name = request.path.split('/')[2]
    game = get_object_or_404(Game, name=game_name)
    try:
        profile = Profile.objects.get(user_id=request.user.id)
        user = User.objects.get(id=request.user.id)
        user_type = profile.profile_type
    except Profile.DoesNotExist:
        return redirect('/accounts/')
    # if user_type == 'DEV':
    #     context['dev'] = 'True'
        # return redirect('/accounts/my_profile/', context)

    if profile.ownedGames.filter(id__exact=game.id).count() > 0:
        source = game.url
        if GameState.objects.filter(game_id_id=game.id):
            game_state = GameState.objects.filter(game_id_id=game.id).order_by('-max_score')[:10]
            context['rank_table'] = 'True'
            context['game_state'] = game_state
        else:
            context['rank_table'] = 'False'
            context['game_state'] = None

        if request.is_ajax():

            if request.POST.get('messageType', None) == 'SCORE':
                form = GameScoreForm(request.POST)
                if form.is_valid():
                    # score = request.POST.get('score', None)
                    score = form.cleaned_data['score']
                    score = float(score)
                    result = {}
                    try:
                        game_state_object = GameState.objects.get(game_id_id=game.id, player_id_id= request.user.id)
                        max_score = game_state_object.max_score
                        if max_score < score:
                            setattr(game_state_object, 'max_score', score)
                            game_state_object.save(force_update=True, update_fields=['max_score'])
                            result['result'] = 'max_score updated'
                        else:
                            result['result'] = 'max_score not changed'
                    except GameState.DoesNotExist:
                        game_state_object = GameState(max_score=score, player_id=user, game_id=game)
                        game_state_object.save()
                        result['result'] = 'max_score saved'

                    result['error'] = False
                    return JsonResponse({'result': result})

            elif request.POST.get('messageType', None) == 'LOAD_REQUEST':
                game_state_objects = GameState.objects.filter(game_id_id = game.id, player_id_id = request.user.id)
                for G_S_OBEJCT in game_state_objects:
                    data = {'messageType': 'LOAD',
                        'gameState': G_S_OBEJCT.gameState,
                        }
                    return JsonResponse(data)
                data = {'messageType': 'LOAD',
                        'gameState': 'None',
                        }
                return JsonResponse(data)

            elif request.POST.get('messageType', None) == 'SAVE':
                form = GameStateForm(request.POST)
                if form.is_valid():
                    if not request.POST.get('score', None) is None:
                        # score = float(request.POST.get('score', None))
                        score = form.cleaned_data['score']
                    else:
                        score = float(0)
                    # game_state = str(request.POST.get('gameState', None))
                    game_state = str(form.cleaned_data['gameState'])
                    result = {}

                    try:
                        game_state_object = GameState.objects.get(game_id_id=game.id, player_id_id=request.user.id)
                        max_score = game_state_object.max_score
                        if max_score < score:
                            setattr(game_state_object, 'max_score', score)
                            setattr(game_state_object, 'gameState', game_state)
                            game_state_object.save(force_update=True, update_fields=['max_score', 'gameState'])
                            result['result'] = 'update game_state saved'
                        else:
                            setattr(game_state_object, 'gameState', game_state)
                            game_state_object.save(force_update=True, update_fields=['gameState'])
                            result['result'] = 'update game_state saved'
                    except GameState.DoesNotExist:
                        game_state_object = GameState(max_score=score, gameState=game_state, player_id=user, game_id=game)
                        game_state_object.save()
                        result['result'] = 'new game_state saved'

                    result['error'] = False
                    return JsonResponse({'result': result})

        if source.endswith('/'):
            source = source[:-1]

        context['source'] = source
        return render(request, "playing_area/playgame.html", context)

    else:
        items = request.session.get('shopping_cart_items', [])
        if not game.id in items:
            items.append(game.id)
            request.session['shopping_cart_items'] = items
        return redirect('/purchase/shopping_cart/')

