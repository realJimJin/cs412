# mini_insta/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Post, Photo

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['caption']

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image_file']

class UpdateProfileForm(forms.ModelForm):
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

# NEW: used by UserRegistrationView
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    display_name = forms.CharField(max_length=150, required=True, label="Display name")
    bio_text = forms.CharField(widget=forms.Textarea, required=False, label="Bio")
    profile_image_url = forms.URLField(required=False, label="Profile image URL")

class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["username", "display_name", "bio_text", "profile_image_url"]
        labels = {
            "username": "Username (handle)",
            "display_name": "Display name",
            "bio_text": "Bio",
            "profile_image_url": "Profile image URL",
        }

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2", "display_name", "bio_text", "profile_image_url")
