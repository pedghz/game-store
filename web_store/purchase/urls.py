from django.conf.urls import url
from . import views


urlpatterns = [

    url(r'^owned_game/$', views.owned_game, name='owned_game'),
    url(r'^shopping_cart/$', views.shopping_cart, name='shopping_cart'),
    url(r'^order/$', views.order, name='order'),
    url(r'^order_details/(?P<order_id>[a-zA-Z0-9]+)/$', views.order_details, name='order_details'),
    url(r'^payment_result/$', views.payment_result, name='payment_result'),
    url(r'^finish_payment/$', views.finish_payment, name='finish_payment'),
    # url(r'^developer_games/$', views.developer_games, name='developer_games'),
]