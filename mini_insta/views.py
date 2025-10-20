
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from .models import Profile, Post, Photo 
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .forms import CreatePostForm, PhotoForm, UpdateProfileForm, UpdatePostForm 
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from django.db.models import Q

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
   
class UpdateProfileView(UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"
    # No need to define get_success_url if Profile.get_absolute_url() exists


class DeletePostView(DeleteView):
    model = Post
    template_name = "mini_insta/delete_post_form.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        post = self.get_object()
        ctx["post"] = post
        ctx["profile"] = post.profile
        return ctx

    def get_success_url(self):
        post = self.get_object()
        return reverse("mini_insta:show_profile", kwargs={"pk": post.profile.pk})


class UpdatePostView(UpdateView):
    model = Post
    form_class = UpdatePostForm
    template_name = "mini_insta/update_post_form.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["profile"] = self.get_object().profile
        return ctx

    def get_success_url(self):
        post = self.get_object()
        return reverse("mini_insta:show_post", kwargs={"pk": post.pk})

class ShowFollowersDetailView(DetailView):
    """Display a Profile and the list of Profiles who follow it."""
    model = Profile
    template_name = "mini_insta/show_followers.html"
    context_object_name = "profile"  # template gets `profile`

class ShowFollowingDetailView(DetailView):
    """Display a Profile and the list of Profiles this Profile follows."""
    model = Profile
    template_name = "mini_insta/show_following.html"
    context_object_name = "profile"

class PostFeedListView(ListView):
    """Feed of posts from profiles that this profile follows."""
    template_name = "mini_insta/show_feed.html"
    context_object_name = "posts"
    paginate_by = 10  # optional: add pagination

    def dispatch(self, request, *args, **kwargs):
        self.profile = get_object_or_404(Profile, pk=self.kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.profile.get_post_feed()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["profile"] = self.profile
        return ctx

class SearchView(ListView):
    """Search Posts (by caption) and Profiles (by username/display_name/bio)."""
    template_name = "mini_insta/search_results.html"
    context_object_name = "posts"  # the ListView queryset name

    def dispatch(self, request, *args, **kwargs):
        # who is doing the search
        self.profile = get_object_or_404(Profile, pk=self.kwargs["pk"])
        self.query = request.GET.get("q")
        # If no query yet, show the search form page
        if not self.query:
            return render(request, "mini_insta/search.html", {"profile": self.profile})
        # Otherwise proceed to results
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # Return matching Posts when a query is present
        return (
            Post.objects
            .filter(caption__icontains=self.query)
            .select_related("profile")
            .order_by("-timestamp")
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["profile"] = self.profile
        ctx["query"] = self.query or ""
        # Profiles that match (username, display_name, or bio_text)
        ctx["profile_results"] = Profile.objects.filter(
            Q(username__icontains=self.query) |
            Q(display_name__icontains=self.query) |
            Q(bio_text__icontains=self.query)
        ).order_by("display_name")
        return ctx
