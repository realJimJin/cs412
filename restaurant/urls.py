from django.urls import path 
from django.conf import settings 
from . import views

#URL patterns specific to the restaurant app:

urlpatterns = [
 path(r'', views.home, name="home"),
 path(r'main', views.main, name="main_page"),
path(r'order', views.order, name="order_page"),
path(r'confirmation', views.confirmation, name="confirmation"),
]

