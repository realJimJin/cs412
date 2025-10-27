from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import (
    ProfileListView, ProfileDetailView, PostDetailView,
    FollowersDetailView, FollowingDetailView,
    MyProfileDetailView, CreatePostView, UpdateProfileView,
    UpdatePostView, DeletePostView, PostFeedListView, SearchView,
    LoginView, LogoutView, UserRegistrationView, CreateProfileView,  # <-- add this
)
app_name = "mini_insta"

urlpatterns = [
    # Public read-only
    path('', views.ProfileListView.as_view(), name="show_all_profiles"),
    path('show_all_profiles', views.ProfileListView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', views.ProfileDetailView.as_view(), name="show_profile"),
    path('post/<int:pk>', views.PostDetailView.as_view(), name="show_post"),

    # Followers / Following (public)
    path("profile/<int:pk>/followers", views.ShowFollowersDetailView.as_view(), name="show_followers"),
    path("profile/<int:pk>/following", views.ShowFollowingDetailView.as_view(), name="show_following"),

    # Owned (require login) – no pk in URL
    path("profile", views.MyProfileDetailView.as_view(), name="my_profile"),
    path("profile/create_post", views.CreatePostView.as_view(), name="create_post"),
    path("profile/update", views.UpdateProfileView.as_view(), name="update_profile"),
    path("profile/feed", views.PostFeedListView.as_view(), name="show_feed"),
    path("profile/search", views.SearchView.as_view(), name="search"),

    # Post edit/delete
    path("post/<int:pk>/update", views.UpdatePostView.as_view(), name="update_post"),
    path("post/<int:pk>/delete", views.DeletePostView.as_view(), name="delete_post"),

    # Auth
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("register/", views.UserRegistrationView.as_view(), name="register"),

    path("create_profile/", CreateProfileView.as_view(), name="create_profile"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
