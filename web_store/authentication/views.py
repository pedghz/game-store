from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.contrib.auth.models import User
from authentication.forms import LoginForm, RegisterForm, AddGame, AccountSettings, ResetPassword, EditGame
from playing_area.models import Game
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.conf import settings
from .models import Profile


def login_register_page(request):
    # This view checks whether the user is authenticated. If not it shows the login page.
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        context = {'login_form': LoginForm(), 'register_form': RegisterForm()}
        return render(request, "registration/login_register.html", context)


def login_view(request):
    # This view handles the login of the user and checks if the user really exists in the database.
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    error = False
    # We use the context because we have several forms in the same page.
    context = {'login_form': LoginForm(request.POST), 'register_form': RegisterForm()}

    # if the method is POST.
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            # We get the cleaned data.
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            #             data is correct.
            if user:
                # If the user really exists, we login
                login(request, user)
                context['error_login'] = error
                return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                # An error will be shown.
                error = True
                context['error_login'] = error
        else:
            context['error_message'] = form._errors["password_reg"]

    else:
        form = LoginForm()

    # context['user_is_authenticated'] = request.user.is_authenticated()
    return render(request, 'registration/login_register.html', context)


def logout_view(request):
    # Loging out is straight forward.
    logout(request)
    # return render(request, 'playing_area/index.html', locals())
    return redirect(settings.LOGIN_REDIRECT_URL)


def register_view(request):
    # This view registers new users.
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    error_register = False
    # We use the context because we have two forms in the same page.
    context = {'login_form': LoginForm(), 'register_form': RegisterForm(request.POST), 'error_register': error_register}

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Getting the form data.
            first_name_reg = form.cleaned_data["first_name_reg"]
            last_name_reg = form.cleaned_data["last_name_reg"]
            username_reg = form.cleaned_data["username_reg"]
            email_reg = form.cleaned_data["email_reg"]
            password_reg = form.cleaned_data["password_reg"]
            account_type = form.cleaned_data["account_type"]

            # Checking if the user already exits.
            user = authenticate(username=username_reg, password=password_reg)
            if user:
                error_register = True
                context['error_register'] = error_register
                context['error_message'] = '* Username already exists.'
            else:
                # Creating the new user.
                new_user = User.objects.create_user(username_reg, email_reg, password_reg)
                new_user.first_name = first_name_reg
                new_user.last_name = last_name_reg
                new_user.save()

                # Every user has a profile. We create a profile and save it.
                new_profile = Profile.objects.create(user=new_user)
                new_profile.profile_type = account_type
                new_profile.save()
                # Authenticating the user.
                user = authenticate(username=username_reg, password=password_reg)
                # data is correct (It should be correct in this case).
                if user:
                    login(request, user)
                    return redirect(settings.LOGIN_REDIRECT_URL)
                else:
                    error_register = True
                    context['error_register'] = error_register
        else:
            error_register = True
            context['error_register'] = error_register
            try:
                context['error_message'] = form._errors["password_reg"]
            except KeyError:
                try:
                    context['error_message'] = form._errors["email_reg"]
                except KeyError:
                    context['error_message'] = form._errors["username_reg"]

    else:
        form = RegisterForm()
        error_register = True
        context['error_register'] = error_register

    return render(request, 'registration/login_register.html', context)

# Here we get the form for adding a game
@login_required
def add_game(request):
    context = {'add_game_form': AddGame(request.POST)}

    try:
        developer = Profile.objects.get(user_id=request.user.id)
        user_type = developer.profile_type
    except Profile.DoesNotExist:
        return redirect('/accounts/')

    # Only developers have access to uploading form for the game
    if user_type == 'DEV':
        if request.method == "POST":
            form = AddGame(request.POST)
            # Form should be valid and clean
            if form.is_valid():
                game_name = form.cleaned_data["game_name"]
                game_url = form.cleaned_data["game_url"]
                price = form.cleaned_data["price"]
                image_url = form.cleaned_data["image_url"]
                genre = form.cleaned_data["genre"]

                # Try to get the row from db, ir if it does not exist create it
                obj, created = Game.objects.get_or_create(
                    name=game_name.lower().replace(' ', '-'),
                    defaults={'url': game_url,
                              'price': price,
                              'image_url': image_url,
                              'genre': genre,
                              'developer': developer,
                              }
                )
                if not created:
                    context['error_register'] = 'True'
                    context['error_message'] = "***Game's name already exists***"
                else:
                    context['error_register'] = 'Sent'
                    # add this game to developer's list of owned games
                    developer.ownedGames.add(obj)
            else:
                context['error_register'] = 'True'
                context['error_message'] = 'The form is not valid!'
        else:
            form = AddGame()
        return render(request, 'registration/upload_game.html', context)
    else:
        return redirect('/accounts/my_profile/')


@login_required
def my_profile(request):
    user = None
    if request.user.is_authenticated():
        user = User.objects.get(id=request.user.id)

    if request.method == 'POST':
        context = {'my_profile_form': AccountSettings(request.POST), 'reset_password_form': ResetPassword()}
        form = AccountSettings(request.POST)
        if form.is_valid():
            # We alter the fields that were changed.
            user.first_name = form.cleaned_data["first_name_settings"]
            user.last_name = form.cleaned_data["last_name_settings"]
            user.email = form.cleaned_data["email_settings"]
            user.save()
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            context = {'my_profile_form': AccountSettings(initial={
                'username_settings': user.username,
                'first_name_settings': user.first_name,
                'last_name_settings': user.last_name,
                'email_settings': user.email
            }), 'reset_password_form': ResetPassword()}
    else:
        context = {'my_profile_form': AccountSettings(initial={
            'username_settings': user.username,
            'first_name_settings': user.first_name,
            'last_name_settings': user.last_name,
            'email_settings': user.email
        }), 'reset_password_form': ResetPassword()}

    if request.user.is_authenticated():
        try:
            user_type = Profile.objects.get(user_id=request.user.id).profile_type
        except User.DoesNotExist:
            return redirect('/accounts/')
        if user_type == 'DEV':
            context['dev'] = 'True'

    return render(request, 'authentication/account_settings.html', context)


def reset_password(request):
    user = None
    if request.user.is_authenticated():
        user = User.objects.get(id=request.user.id)

    if request.method == 'POST':
        context = {'my_profile_form': AccountSettings(), 'reset_password_form': ResetPassword(request.POST)}
        form = ResetPassword(request.POST)
        if form.is_valid():
            # We alter the fields that were changed.
            check = authenticate(username=user.username, password=form.cleaned_data['current_password_settings'])
            if check:
                user.set_password(form.cleaned_data["password_settings"])
                user.save()
                login(request, user)
                return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                error_reset = True
                context['error_reset'] = error_reset
                context['error_message'] = '* Wrong current password.'

        else:
            context = {'my_profile_form': AccountSettings(initial={
                'username_settings': user.username,
                'first_name_settings': user.first_name,
                'last_name_settings': user.last_name,
                'email_settings': user.email
            }), 'reset_password_form': ResetPassword()}
            error_reset = True
            context['error_reset'] = error_reset
            context['error_message'] = form._errors["password_reg"]

    else:
        context = {'my_profile_form': AccountSettings(initial={
            'username_settings': user.username,
            'first_name_settings': user.first_name,
            'last_name_settings': user.last_name,
            'email_settings': user.email
        }), 'reset_password_form': ResetPassword()}

    return render(request, 'authentication/account_settings.html', context)


@login_required
def developer_games(request):
    context = {}
    if request.method == 'GET':
        dev_games = Game.objects.filter(developer=request.user.profile)
        context['games'] = dev_games
        return render(request, "authentication/developer_games.html", context)


# Access the form for editing the game
@login_required
def edit_game(request):
    try:
        developer = Profile.objects.get(user_id=request.user.id)
        user_type = developer.profile_type
    except Profile.DoesNotExist:
        return redirect('/accounts/')

    # Get the game name from the link
    game_name = request.path.split("-", 1)[1]
    game_name = game_name.rstrip('\/')

    # Get the game object for editing and here we check
    try:
        game = Game.objects.get(name=game_name, developer_id=developer)
    except Game.DoesNotExist:
        return redirect('/accounts/developer_games/')

    if request.method == 'POST':
        # if submit button was pressed
        if 'game-submit' in request.POST:
            context = {'edit_game_form': EditGame(request.POST)}
            form = EditGame(request.POST)
            if form.is_valid():
                # We alter the fields that were changed.
                game.name = form.cleaned_data["game_name_edit"]
                game.price = form.cleaned_data["price_edit"]
                game.url = form.cleaned_data["game_url_edit"]
                game.image_url = form.cleaned_data["image_url_edit"]
                game.genre = form.cleaned_data["genre_edit"]
                game.save()
                context['error_register'] = 'Sent'
            else:
                context = {'edit_game_form': EditGame(initial={
                    'game_name_edit': game.name,
                    'price_edit': game.price,
                    'game_url_edit': game.url,
                    'image_url_edit': game.image_url,
                    'genre_edit': game.genre,
                }), 'error_register': 'True', 'error_message': 'The form is not valid!!1'}
            context['request'] = request.POST
        # if remove button was pressed
        elif 'game-remove' in request.POST:
            game.delete()
            return redirect('/accounts/developer_games/')

    else:
        context = {'edit_game_form': EditGame(initial={
            'game_name_edit': game.name,
            'price_edit': game.price,
            'game_url_edit': game.url,
            'image_url_edit': game.image_url,
            'genre_edit': game.genre,
        })}

    if user_type == 'DEV':
        context['dev'] = 'True'

    context['game_name'] = game_name
    return render(request, 'authentication/edit_game.html', context)
