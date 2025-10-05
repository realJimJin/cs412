
from django.urls import path
from .views import * 

app_name = "mini_insta" 

urlpatterns = [
path('', ProfileListView.as_view(), name="show_all_profiles"), 
path('show_all_profiles', ProfileListView.as_view(), name="show_all_profiles"),
path('profile/<int:pk>', ProfileDetailView.as_view(), name="show_profile"),
path('post/<int:pk>', PostDetailView.as_view(), name="show_post"),  
]
