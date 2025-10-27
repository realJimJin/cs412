# mini_insta/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile, Post, Photo


class CreatePostForm(forms.ModelForm):
    """Create a Post (no URL field anymore)."""
    class Meta:
        model = Post
        fields = ["caption"]


class PhotoForm(forms.ModelForm):
    """Upload a single image file for a Post."""
    class Meta:
        model = Photo
        fields = ["image_file"]


class UpdateProfileForm(forms.ModelForm):
    """Edit profile fields (not username/join_date)."""
    class Meta:
        model = Profile
        fields = ["display_name", "bio_text", "profile_image_url"]
        labels = {
            "display_name": "Display name",
            "bio_text": "Bio",
            "profile_image_url": "Profile image URL",
        }


class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["caption"]
        labels = {"caption": "Caption"}


class CreateProfileForm(forms.ModelForm):
    """Used in the combined registration + profile creation page (Task 3)."""
    class Meta:
        model = Profile
        fields = ["username", "display_name", "bio_text", "profile_image_url"]
        labels = {
            "username": "Username (handle)",
            "display_name": "Display name",
            "bio_text": "Bio",
            "profile_image_url": "Profile image URL",
        }


class UserRegistrationForm(UserCreationForm):
    """
    Used by your separate /register/ path (if you keep it).
    Includes extra non-model fields for Profile; DO NOT put these
    in Meta because the Meta.model is User.
    """
    email = forms.EmailField(required=True)
    display_name = forms.CharField(label="Display name", max_length=150)
    bio_text = forms.CharField(label="Bio", widget=forms.Textarea, required=False)
    profile_image_url = forms.URLField(label="Profile image URL", required=False)

    class Meta:
        model = User
        # Only fields that actually exist on User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        # Standard UserCreationForm save, but ensure email is stored
        user = super().save(commit=False)
        user.email = self.cleaned_data.get("email")
        if commit:
            user.save()
        return user
