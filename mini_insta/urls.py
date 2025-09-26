
from django.urls import path
from .views import * 

urlpatterns = [
path('show_all_profiles', ProfileListView.as_view(), name="show_all_profiles"), 
]
