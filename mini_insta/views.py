
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from .models import Profile, Post, Photo 
from django.views.generic import ListView, DetailView, CreateView
from .forms import CreatePostForm, PhotoForm 
from django.urls import reverse
from django.views.generic import UpdateView
from .forms import UpdateProfileForm
from .models import Profile


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
    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def get_success_url(self):
        return reverse('mini_insta:show_profile', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        ctx['profile'] = profile
        # provide photo_form in both GET and POST
        if self.request.method == "POST":
            ctx['photo_form'] = PhotoForm(self.request.POST, self.request.FILES)
        else:
            ctx['photo_form'] = PhotoForm()
        return ctx

    def post(self, request, *args, **kwargs):
        """Process both the Post form and the Photo form together."""
        self.object = None
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])

        form = self.get_form()  # CreatePostForm bound to POST
        photo_form = PhotoForm(request.POST, request.FILES)

        if form.is_valid() and photo_form.is_valid():
            # Save Post
            post = form.save(commit=False)
            post.profile = profile
            post.save()

            # Save Photo only if a file was provided
            if photo_form.cleaned_data.get('image_file'):
                photo = photo_form.save(commit=False)
                photo.post = post
                photo.save()

            return redirect(self.get_success_url())

        # Re-render with errors and the missing context vars
        return render(request, self.template_name, {
            'form': form,
            'photo_form': photo_form,
            'profile': profile,
        })
   
