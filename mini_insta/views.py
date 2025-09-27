
from django.shortcuts import render
from .models import Profile 
from django.views.generic import ListView, DetailView

# Create your views here.
class ProfileListView(ListView):
    '''Define a view class to show all instagram profiles.'''
    
    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"


class ProfileView(DetailView):
    '''Display a single profile.'''

    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile" # note singular variable name
