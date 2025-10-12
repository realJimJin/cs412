# mini_insta/forms.py
# define the forms that we use for create/update/delete operations

from django import forms
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
