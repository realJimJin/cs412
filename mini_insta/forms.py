# mini_insta/forms.py
# define the forms that we use for create/update/delete operations

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Post, Photo 

class CreatePostForm(forms.ModelForm):
    '''A form to add a post to the database.'''
    
    image_url = forms.URLField(required=False, label="Photo URL")
    class Meta:
        '''associate this form with a model from our database.'''
        model = Post
        fields = ['caption']


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image_file']   # upload only


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        # All editable fields EXCEPT username and join_date
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


# ---------- NEW for Task 2: Registration ----------
class UserRegistrationForm(UserCreationForm):
    """Form to register a new user and capture profile info."""
    email = forms.EmailField(required=True)
    display_name = forms.CharField(max_length=100, required=True)
    bio_text = forms.CharField(widget=forms.Textarea, required=False)
    profile_image_url = forms.URLField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
