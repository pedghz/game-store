from django.shortcuts import render
from django.http import HttpResponse




def shopping_cart(request):
    return render(request, "purchase/shopping_cart.html")
