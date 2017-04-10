from django.conf.urls import url
from . import views


urlpatterns = [

    #public
    url(r'^shopping_cart/$', views.shopping_cart, name='shopping_cart'),

    #private


    #Developers
]