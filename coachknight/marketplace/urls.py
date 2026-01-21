from django.urls import path
from . import views

app_name = 'marketplace'

urlpatterns = [
    # Coach intake flow
    path('coaches/join/', views.coach_join, name='coach_join'),
    path('coaches/intake/', views.coach_intake, name='coach_intake'),
    path('coaches/intake/success/', views.coach_intake_success, name='coach_intake_success'),
    path('coaches/dashboard/', views.coach_dashboard, name='coach_dashboard'),
    
    # Vendor waitlist flow
    path('vendors/join/', views.vendor_join, name='vendor_join'),
    path('vendors/join/success/', views.vendor_join_success, name='vendor_join_success'),
    
    # Staff admin
    path('staff/overview/', views.staff_overview, name='staff_overview'),
    path('staff/coaches/', views.staff_coaches, name='staff_coaches'),
    
    # Existing routes
    path('search/', views.search_coaches, name='search'),
    path('coach/<int:pk>/', views.coach_detail, name='coach_detail'),
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/create/', views.job_create, name='job_create'),
    path('jobs/<int:pk>/', views.job_detail, name='job_detail'),
    path('jobs/<int:pk>/edit/', views.job_edit, name='job_edit'),
    path('vendor/dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
]
