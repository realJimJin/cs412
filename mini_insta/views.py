from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.db.models import Q

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views

from .models import Profile, Post, Photo
from .forms import CreatePostForm, PhotoForm, UpdateProfileForm, UpdatePostForm

# --- Small helper mixins so views can find "my" Profile and enforce ownership ---

class MustBeLoggedIn(LoginRequiredMixin):
    login_url = "mini_insta:login"

    def get_current_profile(self):
        """Return the Profile belonging to the logged-in User."""
        return get_object_or_404(Profile, user=self.request.user)


class MustOwnPost(MustBeLoggedIn):
    """Ensure the current user owns the Post being edited/deleted."""
    def dispatch(self, request, *args, **kwargs):
        resp = super().dispatch(request, *args, **kwargs)
        post = getattr(self, "object", None) or self.get_object()
        if post.profile.user != request.user:
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden("You don't have permission for this post.")
        return resp


# ---------------- Public (read-only) views ----------------

class ProfileListView(ListView):
    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"


class ProfileDetailView(DetailView):
    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"


class PostDetailView(DetailView):
    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post"


# ---------------- Owned views (require login, no pk in URL) ----------------

class MyProfileDetailView(MustBeLoggedIn, DetailView):
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"

    def get_object(self):
        return self.get_current_profile()


class CreatePostView(MustBeLoggedIn, CreateView):
    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["profile"] = self.get_current_profile()
        ctx["photo_form"] = PhotoForm(self.request.POST or None, self.request.FILES or None)
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = None
        profile = self.get_current_profile()

        form = self.get_form()
        photo_form = PhotoForm(request.POST, request.FILES)

        if form.is_valid() and photo_form.is_valid():
            post = form.save(commit=False)
            post.profile = profile
            post.save()

            if photo_form.cleaned_data.get("image_file"):
                photo = photo_form.save(commit=False)
                photo.post = post
                photo.save()

            return redirect(reverse("mini_insta:show_post", kwargs={"pk": post.pk}))

        return render(request, self.template_name, {
            "form": form,
            "photo_form": photo_form,
            "profile": profile,
        })


class UpdateProfileView(MustBeLoggedIn, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"

    def get_object(self):
        return self.get_current_profile()


class UpdatePostView(MustOwnPost, UpdateView):
    model = Post
    form_class = UpdatePostForm
    template_name = "mini_insta/update_post_form.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["profile"] = self.get_object().profile
        return ctx

    def get_success_url(self):
        return reverse("mini_insta:show_post", kwargs={"pk": self.get_object().pk})


class DeletePostView(MustOwnPost, DeleteView):
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
        return reverse("mini_insta:my_profile")


class PostFeedListView(MustBeLoggedIn, ListView):
    template_name = "mini_insta/show_feed.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        me = self.get_current_profile()
        # assumes you implemented Profile.get_post_feed() that returns a QS
        return me.get_post_feed().order_by("-timestamp").select_related("profile")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["profile"] = self.get_current_profile()
        return ctx


class SearchView(MustBeLoggedIn, ListView):
    template_name = "mini_insta/search_results.html"
    context_object_name = "posts"

    def dispatch(self, request, *args, **kwargs):
        self.me = self.get_current_profile()
        self.query = request.GET.get("q")
        if not self.query:
            return render(request, "mini_insta/search.html", {"profile": self.me})
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return (Post.objects
                .filter(caption__icontains=self.query)
                .select_related("profile")
                .order_by("-timestamp"))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["profile"] = self.me
        ctx["query"] = self.query or ""
        ctx["profile_results"] = Profile.objects.filter(
            Q(username__icontains=self.query) |
            Q(display_name__icontains=self.query) |
            Q(bio_text__icontains=self.query)
        ).order_by("display_name")
        return ctx


# ---------------- Auth views (templates: login.html) ----------------

class LoginView(auth_views.LoginView):
    template_name = "mini_insta/login.html"

class LogoutView(auth_views.LogoutView):
    next_page = "mini_insta:show_all_profiles"
