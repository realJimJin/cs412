
from django.urls import path 
from django.conf import settings 
from . import views 

#URL patterns specific to the quotes app: 

urlpatterns = [
 #path(r'', views.home, name="home"),
 path(r'about', views.about, name="about_page"),  
]
