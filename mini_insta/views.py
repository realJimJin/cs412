
from django.shortcuts import render
from .models import Profile 
from django.views.generic import ListView

# Create your views here.
class ProfileListView(ListView):
    '''Define a view class to show all instagram profiles.'''
    
    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"

    def dispatch(self, request, *args, **kwargs):
        '''Override the dispatch method to add debugging information.'''

        if request.user.is_authenticated:
            print(f'ProfileListView.dispatch(): request.user={request.user}')
        else:
            print(f'ProfileListView.dispatch(): not logged in.')

        return super().dispatch(request, *args, **kwargs)
