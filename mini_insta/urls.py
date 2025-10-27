# mini_insta/urls.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from .views import (
    ProfileListView, ProfileDetailView, PostDetailView,
    MyProfileDetailView, UpdateProfileView, CreatePostView,
    PostFeedListView, SearchView,
    UpdatePostView, DeletePostView,
    FollowersDetailView, FollowingDetailView,  # <-- note names
)

app_name = "mini_insta"

urlpatterns = [
    # Public
    path('', ProfileListView.as_view(), name="show_all_profiles"),
    path('show_all_profiles', ProfileListView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name="show_profile"),
    path('post/<int:pk>', PostDetailView.as_view(), name="show_post"),

    # Followers / Following (public)
    path("profile/<int:pk>/followers", FollowersDetailView.as_view(), name="show_followers"),
    path("profile/<int:pk>/following", FollowingDetailView.as_view(), name="show_following"),

    # Authenticated “my …” (no pk)
    path("profile", MyProfileDetailView.as_view(), name="my_profile"),
    path("profile/update", UpdateProfileView.as_view(), name="update_profile"),
    path("profile/create_post", CreatePostView.as_view(), name="create_post"),
    path("profile/feed", PostFeedListView.as_view(), name="show_feed"),
    path("profile/search", SearchView.as_view(), name="search"),

    # Post management
    path("post/<int:pk>/update", UpdatePostView.as_view(), name="update_post"),
    path("post/<int:pk>/delete", DeletePostView.as_view(), name="delete_post"),

    # Auth
    path("login/", LoginView.as_view(template_name="mini_insta/login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="mini_insta:show_all_profiles"), name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
