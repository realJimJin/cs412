# mini_insta/urls.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views  # <— import the module, not names

app_name = "mini_insta"

urlpatterns = [
    path('', views.ProfileListView.as_view(), name="show_all_profiles"),
    path('show_all_profiles', views.ProfileListView.as_view(), name="show_all_profiles"),

    # public
    path('profile/<int:pk>', views.ProfileDetailView.as_view(), name="show_profile"),
    path('post/<int:pk>', views.PostDetailView.as_view(), name="show_post"),
    path("profile/<int:pk>/followers", views.ShowFollowersDetailView.as_view(), name="show_followers"),
    path("profile/<int:pk>/following", views.ShowFollowingDetailView.as_view(), name="show_following"),

    # owned (no pk in URL)
    path("profile", views.MyProfileDetailView.as_view(), name="my_profile"),
    path("profile/create_post", views.CreatePostView.as_view(), name="create_post"),
    path("profile/update", views.UpdateProfileView.as_view(), name="update_profile"),
    path("profile/feed", views.PostFeedListView.as_view(), name="show_feed"),
    path("profile/search", views.SearchView.as_view(), name="search"),

    # post edit/delete
    path("post/<int:pk>/delete", views.DeletePostView.as_view(), name="delete_post"),
    path("post/<int:pk>/update", views.UpdatePostView.as_view(), name="update_post"),

    # auth
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("register/", views.UserRegistrationView.as_view(), name="register"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
