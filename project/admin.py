from django.contrib import admin
from .models import Team, Student, CategoryStrength, Meet, RoundAssignment


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "school_name", "coach_name", "coach_email")


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "team", "grade", "active")
    list_filter = ("team", "grade", "active")
    search_fields = ("first_name", "last_name")


@admin.register(CategoryStrength)
class CategoryStrengthAdmin(admin.ModelAdmin):
    list_display = ("student", "category_name", "strength_score")
    list_filter = ("category_name",)
    search_fields = ("student__first_name", "student__last_name")


@admin.register(Meet)
class MeetAdmin(admin.ModelAdmin):
    list_display = ("team", "date", "location")
    list_filter = ("team", "date")


@admin.register(RoundAssignment)
class RoundAssignmentAdmin(admin.ModelAdmin):
    list_display = (
        "meet",
        "round_number",
        "category_name",
        "student",
        "role",
        "score",
    )
    list_filter = ("meet", "round_number", "category_name", "role")
