from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('thread/<int:pk>/', views.thread_detail, name='thread_detail'),
    path('thread/<int:pk>/send/', views.send_message, name='send_message'),
    path('start/coach/<int:coach_pk>/', views.start_thread_with_coach, name='start_thread'),
    path('start/vendor/<int:vendor_pk>/', views.start_thread_with_vendor, name='start_vendor_thread'),
]
