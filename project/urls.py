from django.urls import path

from . import views

app_name = "project"

urlpatterns = [
    # Teams
    path("teams/", views.TeamListView.as_view(), name="team_list"),
    path("teams/add/", views.TeamCreateView.as_view(), name="team_add"),
    path("teams/<int:pk>/edit/", views.TeamUpdateView.as_view(), name="team_edit"),
    path("teams/<int:pk>/delete/", views.TeamDeleteView.as_view(), name="team_delete"),

    # Meets (optionally filtered by team)
    path("teams/<int:team_id>/meets/", views.MeetListView.as_view(), name="team_meets"),
    path("teams/<int:team_id>/meets/add/", views.MeetCreateView.as_view(), name="meet_add"),
    path("meets/", views.MeetListView.as_view(), name="meet_list"),
    path("meets/<int:pk>/", views.MeetDetailView.as_view(), name="meet_detail"),
    path("meets/<int:pk>/edit/", views.MeetUpdateView.as_view(), name="meet_edit"),
    path("meets/<int:pk>/delete/", views.MeetDeleteView.as_view(), name="meet_delete"),

    # Lineup editing
    path("meets/<int:pk>/edit_lineup/", views.EditLineupView.as_view(), name="edit_lineup"),
]
