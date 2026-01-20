from django.urls import path
from . import views

app_name = 'marketplace'

urlpatterns = [
    path('search/', views.search_coaches, name='search'),
    path('coach/<int:pk>/', views.coach_detail, name='coach_detail'),
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/create/', views.job_create, name='job_create'),
    path('jobs/<int:pk>/', views.job_detail, name='job_detail'),
    path('jobs/<int:pk>/edit/', views.job_edit, name='job_edit'),
    path('vendor/dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
]
