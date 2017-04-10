from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.contrib.auth.models import User
from authentication.forms import LoginForm, RegisterForm, AddGame
from playing_area.models import Game

def login_register_page(request):
    context = {'login_form': LoginForm(), 'register_form': RegisterForm()}
    return render(request, "registration/login_register.html", context)


def login_view(request):
    # For testing purposes. use the following login and logout.
    # username: Maxime
    # Password: m0nsup3rm0td3p4ss3

    error = False
    context = {'login_form': LoginForm(request.POST), 'register_form': RegisterForm()}

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            #             data is correct.
            if user:
                login(request, user)
                context['error_login'] = error
                return render(request, 'playing_area/index.html', context)
            else:
                # An error will be shown.
                error = True
                context['error_login'] = error
        else:
            context['error_message'] = form._errors["password_reg"]

    else:
        form = LoginForm()

    return render(request, 'registration/login_register.html', context)


def logout_view(request):
    logout(request)
    return render(request, 'playing_area/index.html', locals())


def register_view(request):
    error_register = False
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

            # Checking if the user already exits.
            # TODO check the usernames.
            user = authenticate(username=username_reg, password=password_reg)
            if user:
                error_register = True
                context['error_register'] = error_register
                context['error_message'] = '<p style="color: red"><strong>* Username already exists.</strong></p>'
            else:
                # Creating the new user.
                new_user = User.objects.create_user(username_reg, email_reg, password_reg)
                new_user.first_name = first_name_reg
                new_user.last_name = last_name_reg
                new_user.save()
                # Authenticating the user.
                user = authenticate(username=username_reg, password=password_reg)
                # data is correct (It should be correct in this case).
                if user:
                    login(request, user)
                    return render(request, 'playing_area/index.html', context)
                else:
                    error_register = True
                    context['error_register'] = error_register
        else:
            error_register = True
            context['error_register'] = error_register
            try:
                context['error_message'] = form._errors["password_reg"]
            except KeyError:
                context['error_message'] = form._errors["email_reg"]

    else:
        form = RegisterForm()
        error_register = True
        context['error_register'] = error_register

    return render(request, 'registration/login_register.html', context)


def add_game(request):
    context = {'add_game_form': AddGame(request.POST)}

    if request.method == "POST":
        form = AddGame(request.POST)
        if form.is_valid():
            game_name = form.cleaned_data["game_name"]
            game_url = form.cleaned_data["game_url"]
            price = form.cleaned_data["price"]
            image_url = form.cleaned_data["image_url"]
            genre = form.cleaned_data["genre"]

            obj, created = Game.objects.get_or_create(
                name=game_name.lower().replace(' ','-'),
                defaults={'url': game_url,
                          'price': price,
                          'image_url': image_url,
                          'genre': genre,
                          }
            )
            # try:
            #     obj = Game.objects.get(name=game_name)
            #     error_register = True
            #     context['error_register'] = error_register
            #     context['error_message'] = "<p style='color: red'><strong>* Game's name already exists.</strong></p>"
            # except Game.DoesNotExist:
            #     obj = Game(name=game_name, url=game_url, price=price, image_url=image_url, game_version=game_version, genre=genre)
            #     obj.save()
            if not created or obj is None:
                error_register = True
                context['error_register'] = error_register
                context['error_message'] = "***Game's name already exists***"
        else:
            error_register = True
            context['error_register'] = error_register
            context['error_message'] = 'The form is not valid!'
    else:
        form = AddGame()

    return render(request, 'registration/upload_game.html', context)
