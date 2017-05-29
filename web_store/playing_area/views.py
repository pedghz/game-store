from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from playing_area.models import GameState
from playing_area.models import Game
from django.contrib.auth.models import User
from django.shortcuts import redirect
from authentication.forms import AddGame
from playing_area.forms import SearchGame, GameStateForm, GameScoreForm
from django.contrib.auth.decorators import login_required
from authentication.models import Profile


# Home Page shows only last 4 uploaded games
def my_index(request):
    context = {}
    games_list = Game.objects.all().order_by('-date_time')[:4]
    # this counter is used to show game items in the homepage properly
    context['counter'] = 1
    context['games_list'] = games_list

    return render(request, "playing_area/index.html", context)


# This is the page that people see a list of games which could be filtered by
# their genre or someone can search a game's name through this page
def my_gameslist(request):
    context = {}
    context['search_game'] = SearchGame(request.POST)
    context['counter'] = 1
    genre_list = []
    # get a list of genres to show the links on top of screen
    for genre in AddGame.genre_choices:
        genre_list.append(genre[0])
    context['genres'] = genre_list
    if request.method == "POST":
        form = SearchGame(request.POST)
        if form.is_valid():
            keyword = form.cleaned_data["keyword"]
            # replace white spaces with dashes to mimic the way names are stored in db
            keyword = keyword.lower().replace(' ', '-')
            games_list = Game.objects.filter(name__icontains=keyword)
            context['games_list'] = games_list
        else:
            context['error_search'] = 'True'
            context['error_message'] = 'The form is not valid!'
    else:
        # without selecting any genres all games would be shown.
        games_list = Game.objects.all()
        context['games_list'] = games_list
        if request.is_ajax() and request.path.split('/')[2] != '':
            # get the games with selected genre by user from the link
            games_list = Game.objects.filter(genre=request.path.split('/')[2])
            if games_list.count() > 0:
                context['games_list'] = games_list
            else:
                context['games_list'] = {}
            if request.POST.get('messageType', None) is not None:
                genre = request.POST.get('messageType', None)
                games_list = Game.objects.filter(genre=genre)
                if games_list.count() > 0:
                    context['games_list'] = games_list
                else:
                    context['games_list'] = {}
                return render(request, "playing_area/gameslist_genre.html", context)
        if request.path.split('/')[2] != '':
            return render(request, "playing_area/gameslist.html", context)

    return render(request, "playing_area/gameslist.html", context)


@login_required
def playing_game(request):
    context = {}
    # redirect to login page ig user is not logged in and tries to play a game.
    try:
        profile = Profile.objects.get(user_id=request.user.id)
        user = User.objects.get(id=request.user.id)
    except Profile.DoesNotExist:
        return redirect('/accounts/')
    # get the game object from its name in the link
    game_name = request.path.split('/')[2]
    game = get_object_or_404(Game, name=game_name)

    # if only the user has purchased this game he/she can play it
    if profile.ownedGames.filter(id__exact=game.id).count() > 0:
        source = game.url
        if GameState.objects.filter(game_id_id=game.id):
            game_state = GameState.objects.filter(game_id_id=game.id).order_by('-max_score')[:10]
            context['rank_table'] = 'True'
            context['game_state'] = game_state
        else:
            context['rank_table'] = 'False'
            context['game_state'] = None

        # handle ajax requests for score/save/load
        if request.is_ajax():
            # Saving score which is sent from game
            if request.POST.get('messageType', None) == 'SCORE':
                form = GameScoreForm(request.POST)
                # cleaning data sent from the game
                if form.is_valid():
                    score = float(form.cleaned_data['score'])
                    result = {}
                    # if the related game state exists the just update it
                    try:
                        game_state_object = GameState.objects.get(game_id_id=game.id, player_id_id=request.user.id)
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

            # Sending GameState to game.
            elif request.POST.get('messageType', None) == 'LOAD_REQUEST':
                try:
                    game_state_object = GameState.objects.get(game_id_id=game.id, player_id_id=request.user.id)
                    data = {'messageType': 'LOAD',
                            'gameState': game_state_object.gameState,
                            }
                    return JsonResponse(data)
                except GameState.DoesNotExist:
                    data = {'messageType': 'LOAD',
                            'gameState': 'None',
                            }
                return JsonResponse(data)

            # Saving the GameState in db
            elif request.POST.get('messageType', None) == 'SAVE':
                form = GameStateForm(request.POST)
                # cleaning the data sent form the game
                if form.is_valid():
                    if not request.POST.get('score', None) is None:
                        score = float(form.cleaned_data['score'])
                    else:
                        score = float(0)
                    # convert the game state to string to save it in db as string
                    game_state = str(form.cleaned_data['gameState'])
                    result = {}

                    # if the related game state exists the just update it
                    try:
                        game_state_object = GameState.objects.get(game_id_id=game.id, player_id_id=request.user.id)
                        max_score = game_state_object.max_score
                        # update the score if its bigger than the score we have saved before in db
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
                        game_state_object = GameState(max_score=score, gameState=game_state, player_id=user,
                                                      game_id=game)
                        game_state_object.save()
                        result['result'] = 'new game_state saved'

                    result['error'] = False
                    return JsonResponse({'result': result})

        if source.endswith('/'):
            source = source[:-1]

        context['source'] = source
        return render(request, "playing_area/playgame.html", context)

    # if the user does not own the game add the game to his/her cart and redirect to shopping cart page.
    else:
        items = request.session.get('shopping_cart_items', [])
        if not game.id in items:
            items.append(game.id)
            request.session['shopping_cart_items'] = items
        return redirect('/purchase/shopping_cart/')
