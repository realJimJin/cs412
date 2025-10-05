# mini_insta/forms.py
# define the forms that we use for create/update/delete operations

from django import forms
from .models import Profile, Post

class CreatePostForm(forms.ModelForm):
    '''A form to add a post to the database.'''

    class Meta:
        '''associate this form with a model from our database.'''
        model = Post
        fields = ['profile', 'caption', 'timestamp']
