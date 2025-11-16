from django.urls import path
from . import views, api_views   # api_views we'll create next

urlpatterns = [
    path('', views.random_view, name='home'),
    path('random', views.random_view, name='random'),

    path('jokes', views.jokes_list, name='jokes_list'),
    path('joke/<int:pk>', views.joke_detail, name='joke_detail'),

    path('pictures', views.pictures_list, name='pictures_list'),
    path('picture/<int:pk>', views.picture_detail, name='picture_detail'),

    # API endpoints
    path('api/', api_views.random_joke, name='api_root'),
    path('api/random', api_views.random_joke, name='api_random_joke'),
    path('api/jokes', api_views.jokes_list, name='api_jokes'),
    path('api/joke/<int:pk>', api_views.joke_detail, name='api_joke_detail'),
    path('api/pictures', api_views.pictures_list, name='api_pictures'),
    path('api/picture/<int:pk>', api_views.picture_detail, name='api_picture_detail'),
    path('api/random_picture', api_views.random_picture, name='api_random_picture'),
]
