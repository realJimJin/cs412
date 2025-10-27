from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import (
    ListView, DetailView, CreateView, DeleteView, UpdateView, FormView
)
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.contrib.auth import login

from .models import Profile, Post, Photo
from .forms import (
    CreatePostForm, PhotoForm, UpdateProfileForm, UpdatePostForm, UserRegistrationForm, CreateProfileForm, 
)

# --- helper: safe redirect back ---
def _back(request, fallback):
    return redirect(request.META.get("HTTP_REFERER") or fallback)

# ---------- Auth convenience mixins ----------

class MustBeLoggedIn(LoginRequiredMixin):
    login_url = "mini_insta:login"

    def get_current_profile(self):
        return get_object_or_404(Profile, user=self.request.user)

class MustOwnPost(MustBeLoggedIn):
    def dispatch(self, request, *args, **kwargs):
        resp = super().dispatch(request, *args, **kwargs)
        post = getattr(self, "object", None) or self.get_object()
        if post.profile.user != request.user:
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden("You don't have permission for this post.")
        return resp


# ---------- Public (read-only) views ----------

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


# ---------- Owned views (require login; no pk in URL) ----------

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
        return me.get_post_feed().order_by("-timestamp").select_related("profile")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["profile"] = self.get_current_profile()
        return ctx

class CreateProfileView(CreateView):
    template_name = "mini_insta/create_profile_form.html"
    form_class = CreateProfileForm
    model = Profile

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # blank user form on GET; bound on POST if errors
        if self.request.method == "POST":
            ctx["user_form"] = UserCreationForm(self.request.POST)
        else:
            ctx["user_form"] = UserCreationForm()
        return ctx

    def form_valid(self, form):
        # Rebuild the UserCreationForm from POST and validate
        user_form = UserCreationForm(self.request.POST)
        if not user_form.is_valid():
            # Re-render both forms with errors
            return render(self.request, self.template_name, {
                "form": form,
                "user_form": user_form,
            })

        # Create the User
        user = user_form.save()

        # Log them in (DB backend)
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')

        # Attach the user to the Profile instance being created
        form.instance.user = user

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("mini_insta:my_profile")

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


# ---------- Followers/Following (public) ----------

class ShowFollowersDetailView(DetailView):
    model = Profile
    template_name = "mini_insta/show_followers.html"
    context_object_name = "profile"

class ShowFollowingDetailView(DetailView):
    model = Profile
    template_name = "mini_insta/show_following.html"
    context_object_name = "profile"


# ---------- Auth views ----------

class LoginView(auth_views.LoginView):
    template_name = "mini_insta/login.html"

class LogoutView(auth_views.LogoutView):
    next_page = "mini_insta:show_all_profiles"


# ---------- Registration ----------

class UserRegistrationView(FormView):
    template_name = "mini_insta/register.html"
    form_class = UserRegistrationForm

    def form_valid(self, form):
        user = form.save()  # creates User from UserCreationForm fields
        # create linked Profile
        Profile.objects.create(
            user=user,
            username=user.username,
            display_name=form.cleaned_data["display_name"],
            bio_text=form.cleaned_data.get("bio_text", ""),
            profile_image_url=form.cleaned_data.get("profile_image_url", "")
        )
        login(self.request, user)
        return redirect("mini_insta:my_profile")

# ---------- FOLLOW / UNFOLLOW ----------

class FollowCreateView(MustBeLoggedIn, View):
    """Current user follows the profile identified by pk."""
    def post(self, request, pk):
        me = self.get_current_profile()
        target = get_object_or_404(Profile, pk=pk)
        if target == me:
            return HttpResponseForbidden("You cannot follow yourself.")
        Follow.objects.get_or_create(profile=target, follower_profile=me)
        return _back(request, reverse("mini_insta:show_profile", kwargs={"pk": pk}))


class FollowDeleteView(MustBeLoggedIn, View):
    """Current user unfollows the profile identified by pk."""
    def post(self, request, pk):
        me = self.get_current_profile()
        target = get_object_or_404(Profile, pk=pk)
        Follow.objects.filter(profile=target, follower_profile=me).delete()
        return _back(request, reverse("mini_insta:show_profile", kwargs={"pk": pk}))


# ---------- LIKE / UNLIKE ----------

class LikeCreateView(MustBeLoggedIn, View):
    """Current user likes the post identified by pk."""
    def post(self, request, pk):
        me = self.get_current_profile()
        post = get_object_or_404(Post, pk=pk)
        if post.profile_id == me.id:
            return HttpResponseForbidden("You cannot like your own post.")
        Like.objects.get_or_create(post=post, profile=me)
        return _back(request, reverse("mini_insta:show_post", kwargs={"pk": pk}))


class LikeDeleteView(MustBeLoggedIn, View):
    """Current user unlikes the post identified by pk."""
    def post(self, request, pk):
        me = self.get_current_profile()
        post = get_object_or_404(Post, pk=pk)
        Like.objects.filter(post=post, profile=me).delete()
        return _back(request, reverse("mini_insta:show_post", kwargs={"pk": pk}))
