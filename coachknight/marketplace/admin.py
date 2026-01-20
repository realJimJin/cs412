from django.contrib import admin
from .models import Town, CoachProfile, VendorProfile, AvailabilitySlot, CoachTown, JobPost, VendorCoachStatus

@admin.register(Town)
class TownAdmin(admin.ModelAdmin):
    list_display = ['name', 'state', 'created_at']
    search_fields = ['name']

@admin.register(CoachProfile)
class CoachProfileAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'grade_level', 'years_experience', 'has_car', 'actively_looking', 'created_at']
    list_filter = ['grade_level', 'has_car', 'actively_looking', 'created_at']
    search_fields = ['display_name', 'user_profile__user__username', 'school_affiliation']

@admin.register(VendorProfile)
class VendorProfileAdmin(admin.ModelAdmin):
    list_display = ['organization_name', 'contact_name', 'email', 'created_at']
    search_fields = ['organization_name', 'contact_name', 'email']

@admin.register(AvailabilitySlot)
class AvailabilitySlotAdmin(admin.ModelAdmin):
    list_display = ['coach', 'day_of_week', 'start_time', 'end_time']
    list_filter = ['day_of_week']
    search_fields = ['coach__display_name']

@admin.register(CoachTown)
class CoachTownAdmin(admin.ModelAdmin):
    list_display = ['coach', 'town']
    list_filter = ['town']
    search_fields = ['coach__display_name', 'town__name']

@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'vendor', 'town', 'age_group', 'is_active', 'created_at']
    list_filter = ['age_group', 'is_active', 'created_at']
    search_fields = ['title', 'vendor__organization_name', 'town__name']

@admin.register(VendorCoachStatus)
class VendorCoachStatusAdmin(admin.ModelAdmin):
    list_display = ['vendor', 'coach', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['vendor__organization_name', 'coach__display_name']
