
from django.shortcuts import render
from .models import Profile, Post, Photo 
from django.views.generic import ListView, DetailView, CreateView
from .forms import CreatePostForm, PhotoForm 
from django.urls import reverse

# Create your views here.
class ProfileListView(ListView):
    '''Define a view class to show all instagram profiles.'''
    
    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"


class ProfileDetailView(DetailView):
    '''Display a single profile.'''

    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile" # note singular variable name


class PostDetailView(DetailView):
    '''Display a single profile.'''

    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post" # note singular variable name


class CreatePostView(CreateView):
    '''A view to handle creation of a new Post on a profile.'''

    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def get_success_url(self):
        '''Provide a URL to redirect to after creating a new Post.'''

        # create and return a URL:
        # return reverse('show_all') # not ideal; we will return to this
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        # call reverse to generate the URL for this Article
        return reverse('mini_insta:show_profile', kwargs={'pk':pk})

    def get_context_data(self):
        '''Return the dictionary of context variables for use in the template.'''

        # calling the superclass method
        context = super().get_context_data()

        # find/add the profile to the context data
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        # add this profile into the context dictionary:
        context['profile'] = profile
        return context

    def form_valid(self, form):
        '''This method handles the form submission and saves the
        new object to the Django database.
        We need to add the foreign key (of the Profile) to the Post
        object before saving it to the database.
        '''

        print(form.cleaned_data)
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        # attach this profile to the post
        form.instance.profile = profile # set the FK

        # create the Post but don’t commit yet
        self.object = form.save(commit=False)
        self.object.profile = profile
        self.object.save()

       # now create the related Photo
        image_url = form.cleaned_data["image_url"]
        Photo.objects.create(post=self.object, image_url=image_url)

        # delegate the work to the superclass method form_valid:
        return super().form_valid(form)
   
