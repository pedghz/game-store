from django.http.response import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse
from .forms import shoppingCartForm
from playing_area.models import Game
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from datetime import datetime
from .models import Order
from authentication.models import Profile
from django.contrib.auth.decorators import login_required
from hashlib import md5
from django.shortcuts import redirect

#shows list of owned games
@login_required
def owned_game(request):
    games = [x.add_to_json(request.user) for x in request.user.profile.ownedGames.all()]
    return render(request, 'purchase/ownedGame.html', {'user': request.user, 'games': games})


@login_required
def shopping_cart(request):

    #user validation
    try:
        Profile.objects.get(user_id=request.user.id )
    except:
        return redirect('/accounts/login')


    #checks if the request is GET, it adds the game to the session
    if request.method == 'GET':
        game_ids = request.session.get('shopping_cart_items', [])
        return render(request, 'purchase/shopping_cart.html', {'user': request.user, 'cart': add_to_cart(game_ids)})

    #checks if the request is POST, it performs some validation
    elif request.method == 'POST':
        if not request.is_ajax():
            messages.error(request, "The page that you are requesting is only available through ajax call")
            return HttpResponseRedirect(reverse("shopping_cart"))

        jscontainer = {'error': None}

        #validation based on shopping cart form
        form = shoppingCartForm(request.POST)
        if not form.is_valid():
            jscontainer['error'] = form.errors
            return JsonResponse(status=400, data=jscontainer)

        # checks if the game had been bought before or not
        if form.cleaned_data['action'] == 'add':
            owned_games = request.user.profile.ownedGames.filter(id__exact=form.cleaned_data['game'].id)
            if owned_games.count() > 0:
                jscontainer['error'] = "You already own this game"

            curcart = request.session.get('shopping_cart_items', [])

            #checks if the current session has specified game or not
            if form.cleaned_data['game'].id in curcart:
                jscontainer['error'] = "The game is already in your basket"

            if jscontainer['error'] is None:
                curcart.append(form.cleaned_data['game'].id)
                request.session['shopping_cart_items'] = curcart

        elif form.cleaned_data['action'] == 'remove':
            items = request.session.get('shopping_cart_items', [])
            if form.cleaned_data['game'].id in items:
                items.remove(form.cleaned_data['game'].id)
                request.session['shopping_cart_items'] = items

        else:
            jscontainer['error'] = "Action requested is not valid"

        if jscontainer['error'] is not None:
            return JsonResponse(status=400, data=jscontainer)
        else:
            return JsonResponse(status=201, data=jscontainer)

    else:
        return HttpResponse(status=405, content="Invalid method.")


#it gets the specified game form the databse and returns the result in order to add to the cart
def add_to_cart(game_ids,user=None):
    result = dict()
    result['games'] = list()
    result['total'] = 0
    result['quantity'] = 0
    for id in game_ids:
        try:
            game = Game.objects.get(id=id)
            result['games'].append(game.add_to_json(user=user))
            result['total'] += game.price
            result['quantity'] += 1
        except ObjectDoesNotExist:
            messages.error("one item was invalid, please check the game again!")
            continue
    return result


@login_required
def order(request):

    if request.method == 'GET':
        orders = Order.objects.filter(_player=request.user.profile)

        return render(request, 'purchase/order.html', {'orders': orders})
    #collects the games and their info from session
    elif request.method == 'POST':
        game_ids = request.session.get('shopping_cart_items', [])
        total = 0.0
        games = Game.objects.filter(id__in=game_ids)
        #check weather the user has bought the game already or not
        for game in games:
            if request.user.profile.ownedGames.filter(id__exact=game.id).count() > 0:
                messages.error(request, "You already own the game %s. This item has been removed from the cart"
                               % game.name)
                game_ids.remove(game.id)
            else:
                total += game.price

        #if status of the the order is pending, delete it
        Order.objects.filter(_player=request.user.profile, status="pending").delete()

        games = Game.objects.filter(id__in=game_ids)

        if games.count() < 1:
            messages.warning(request, "The cart is empty!")
            return HttpResponseRedirect(reverse("shopping_cart"))

        #creat the order rows in the databse
        order_obj = Order.objects.create(_player=request.user.profile,
                                     total=total,
                                     orderDate=datetime.now(),
                                     paymentDate=None,
                                     paymentRef=None,
                                     status="pending")
        order_obj._games = games.all()
        order_obj.save()

        messages.info(request, "Order created successfully.")

        return HttpResponseRedirect(reverse("order_details", kwargs={'order_id':order_obj.id}))

    else:
        return HttpResponse(status=405, content="Invalid method.")


@login_required
def order_details(request, order_id):
    if request.method == 'GET':
        if order_id is None:
            messages.error(request, "Invalid or missing Pid specified.")
            return HttpResponseRedirect(reverse("shopping_cart"))

        pid = order_id
        order = None

        #validation for user and games and order
        try:
            order = Order.objects.get(id=pid)
        except ObjectDoesNotExist:
            messages.error(request, "Invalid or missing Pid specified.")
            return HttpResponseRedirect(reverse("shopping_cart"))

        if order._player != request.user.profile:
            messages.error(request, "You are not allowed to manage this order")
            return HttpResponseRedirect(reverse("shopping_cart"))

        if order.status != "pending" and order.status != "error":
            messages.error(request, "The specified order is not on a valid status to be processed again.")
            return HttpResponseRedirect(reverse("shopping_cart"))

        #validation with payment service
        action = "https://simplepayments.herokuapp.com/pay/"
        amount = order.total
        sid = "unchained"
        success_url = request.build_absolute_uri(reverse("payment_result"))
        cancel_url = request.build_absolute_uri(reverse("payment_result"))
        error_url = request.build_absolute_uri(reverse("payment_result"))
        secret_key = "9a4b9b18721dc20344dba2bd26b737e3"

        checksumstr = "pid={}&sid={}&amount={}&token={}".format(pid, sid, amount, secret_key)
        m = md5(checksumstr.encode("ascii"))
        checksum = m.hexdigest()

        game_ids = [g.id for g in order._games.all()]

        #assigning the validated data to the buying.html form attribute
        return render(request, 'purchase/buying.html', {'user': request.user,
                                                       'cart':  add_to_cart(game_ids),
                                                       'action': action,
                                                       'pid': pid,
                                                       'sid': sid,
                                                       'amount': amount,
                                                       'success_url': success_url,
                                                       'cancel_url': cancel_url,
                                                       'error_url': error_url,
                                                       'checksum': checksum})

    else:
        return HttpResponse(status=405, content="Invalid method.")


@login_required
def payment_result(request):
    if request.method == 'GET':
        pid = request.GET['pid']
        ref = request.GET['ref']
        result = request.GET['result']
        checksum = request.GET['checksum']

        #checking wether the information from payment service is validated
        sid = "unchained"
        secret_key = "9a4b9b18721dc20344dba2bd26b737e3"
        checksumstr = "pid={}&ref={}&result={}&token={}".format(pid, ref, result, secret_key)
        m = md5(checksumstr.encode("ascii"))
        checksum2 = m.hexdigest()

        if checksum != checksum2:
            messages.error(request, "Invalid checksum. Your payment is invalid.")
            return HttpResponseRedirect(redirect_to=reverse("shopping_cart"))


        order = None
        try:
            order = Order.objects.get(id=pid)
        except ObjectDoesNotExist:
            messages.error(request, "Invalid OrderId specified. Your payment is invalid.")
            return HttpResponseRedirect(redirect_to=reverse("shopping_cart"))

        if order._player != request.user.profile:
            messages.error(request, "The order ID specified is not yours. Your payment is invalid.")
            return HttpResponseRedirect(redirect_to=reverse("shopping_cart"))

        if order.status != "pending":
            messages.error(request, "The order ID specified is not in the pending status. Please make another order.")
            return HttpResponseRedirect(redirect_to=reverse("shopping_cart"))

        if result not in ["success", "cancel", "error"]:
            messages.error(request, "The result parameter is unrecognized.")
            return HttpResponseRedirect(redirect_to=reverse("shopping_cart"))

        #adding the information to the owned game
        if result == "success":
            for g in order._games.all():
                order._player.ownedGames.add(g)
                g.purchased_times += 1
                g.save()
            order._player.save()
            order.status = "success"
            order.paymentRef = ref
            order.paymentDate = datetime.now()
            order.save()

            #removing the current session
            del request.session['shopping_cart_items']

            return HttpResponseRedirect(redirect_to=reverse("finish_payment"))

        elif result == "cancel":
            order.delete()
            messages.info(request,"The order has been canceled as requested.")
            return HttpResponseRedirect(redirect_to=reverse("shopping_cart"))

        elif result == "error":
            order.status = "error"
            messages.error(request,"There was an error processing the payment. Please try again!")
            return HttpResponseRedirect(redirect_to=reverse("order_details", kwargs={'order_id': pid}))


    else:
        return HttpResponse(status=405, content="Invalid method.")

# Redirect the user to the owned game page after purchasing the game.
@login_required
def finish_payment(request):
    messages.success(request, "Thank you for your purchase. Enjoy the new game!")
    return HttpResponseRedirect(reverse('owned_game'))
