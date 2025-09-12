
from django.urls import path 
from django.conf import settings 
from . import views 

#URL patterns specific to the quotes app: 

urlpatterns = [
 path(r'', views.home, name="home"),
 path(r'about', views.about, name="about_page"),
path(r'quote', views.quote, name="quote_page"),
path(r'show_all', views.show_all, name="show_all_page"),  
]
