from django.db import models
from django.contrib.auth.models import User
from accounts.models import UserProfile

class Town(models.Model):
    name = models.CharField(max_length=100, unique=True)
    state = models.CharField(max_length=2, default='MA')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}, {self.state}"

class CoachProfile(models.Model):
    GRADE_CHOICES = [
        ('hs', 'High School'),
        ('college', 'College'),
        ('other', 'Other'),
    ]
    AGE_GROUPS = [
        ('k2', 'K-2'),
        ('35', '3-5'),
        ('68', '6-8'),
        ('912', '9-12'),
    ]
    
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    school_affiliation = models.CharField(max_length=200, blank=True)
    grade_level = models.CharField(max_length=10, choices=GRADE_CHOICES)
    
    # Chess rating
    rating_rapid = models.IntegerField(null=True, blank=True)
    rating_blitz = models.IntegerField(null=True, blank=True)
    rating_bullet = models.IntegerField(null=True, blank=True)
    rating_text = models.CharField(max_length=100, blank=True, help_text="Free text rating description")
    
    # Experience
    years_experience = models.IntegerField(default=0)
    age_groups_taught = models.CharField(max_length=50, blank=True, help_text="Comma-separated age group codes")
    
    # Preferences
    hourly_rate_min = models.IntegerField(null=True, blank=True)
    hourly_rate_max = models.IntegerField(null=True, blank=True)
    has_car = models.BooleanField(default=False)
    max_travel_miles = models.IntegerField(default=10)
    
    # Badges (checkboxes for MVP)
    references_provided = models.BooleanField(default=False)
    experience_with_schools = models.BooleanField(default=False)
    tournament_director_experience = models.BooleanField(default=False)
    
    # Profile photo
    profile_image = models.ImageField(upload_to='coach_photos/', blank=True, null=True)
    
    # Status
    actively_looking = models.BooleanField(default=True)
    
    # Contact info (hidden by default)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.display_name

    @property
    def user(self):
        return self.user_profile.user

class AvailabilitySlot(models.Model):
    DAY_CHOICES = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]
    
    coach = models.ForeignKey(CoachProfile, on_delete=models.CASCADE, related_name='availability_slots')
    day_of_week = models.IntegerField(choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    def __str__(self):
        return f"{self.get_day_of_week_display()} {self.start_time}-{self.end_time} ({self.coach.display_name})"

class CoachTown(models.Model):
    coach = models.ForeignKey(CoachProfile, on_delete=models.CASCADE, related_name='coach_towns')
    town = models.ForeignKey(Town, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.coach.display_name} serves {self.town.name}"

class VendorProfile(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    organization_name = models.CharField(max_length=200)
    contact_name = models.CharField(max_length=100)
    email = models.EmailField()
    website = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.organization_name

    @property
    def user(self):
        return self.user_profile.user

class JobPost(models.Model):
    AGE_GROUP_CHOICES = [
        ('k2', 'K-2'),
        ('35', '3-5'),
        ('68', '6-8'),
        ('912', '9-12'),
    ]
    
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE, related_name='job_posts')
    town = models.ForeignKey(Town, on_delete=models.CASCADE)
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Schedule
    days_of_week = models.CharField(max_length=50, help_text="Comma-separated day numbers (0=Monday)")
    start_time = models.TimeField()
    end_time = models.TimeField()
    start_date = models.DateField()
    
    # Job details
    age_group = models.CharField(max_length=10, choices=AGE_GROUP_CHOICES)
    num_students = models.IntegerField()
    pay_rate_min = models.IntegerField(null=True, blank=True)
    pay_rate_max = models.IntegerField(null=True, blank=True)
    
    # Requirements
    requires_car = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} at {self.vendor.organization_name}"

class VendorCoachStatus(models.Model):
    STATUS_CHOICES = [
        ('contacted', 'Contacted'),
        ('interviewing', 'Interviewing'),
        ('hired', 'Hired'),
        ('not_a_fit', 'Not a Fit'),
    ]
    
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE)
    coach = models.ForeignKey(CoachProfile, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['vendor', 'coach']

    def __str__(self):
        return f"{self.coach.display_name} - {self.get_status_display()} ({self.vendor.organization_name})"
