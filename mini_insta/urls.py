from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    # public (read-only)
    ProfileListView, ProfileDetailView, PostDetailView,
    FollowersDetailView, FollowingDetailView,

    # owned / auth-required
    MyProfileDetailView, CreatePostView, UpdateProfileView,
    PostFeedListView, SearchView,
    UpdatePostView, DeletePostView,

    # auth endpoints
    LoginView, LogoutView,
)

app_name = "mini_insta"

urlpatterns = [
    # Public pages
    path("", ProfileListView.as_view(), name="show_all_profiles"),
    path("show_all_profiles", ProfileListView.as_view(), name="show_all_profiles"),
    path("profile/<int:pk>", ProfileDetailView.as_view(), name="show_profile"),
    path("post/<int:pk>", PostDetailView.as_view(), name="show_post"),
    path("profile/<int:pk>/followers", FollowersDetailView.as_view(), name="show_followers"),
    path("profile/<int:pk>/following", FollowingDetailView.as_view(), name="show_following"),

    # Logged-in “my” pages (no pk in URL)
    path("profile", MyProfileDetailView.as_view(), name="my_profile"),
    path("profile/create_post", CreatePostView.as_view(), name="create_post"),
    path("profile/update", UpdateProfileView.as_view(), name="update_profile"),
    path("profile/feed", PostFeedListView.as_view(), name="show_feed"),
    path("profile/search", SearchView.as_view(), name="search"),

    # Post mutations (still need the Post PK)
    path("post/<int:pk>/update", UpdatePostView.as_view(), name="update_post"),
    path("post/<int:pk>/delete", DeletePostView.as_view(), name="delete_post"),

    # Auth
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
