from django.db import models

# Create your models here.

class Profile (models.Model):
    '''Encapsulate the data of a user profile on mini_insta.'''

    # define the data attributes of the Article object
    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    bio_text = models.TextField(blank=True) 
    join_date = models.DateTimeField(auto_now=True)
    profile_image_url = models.URLField(blank=True) # url as a string
    #user = models.ForeignKey(User, on_delete=models.CASCADE) 
    def __str__(self):
        '''return a string representation of this model instance.'''
        return f'{self.username} displays as {self.display_name}'


class Post(models.Model):
    '''Encapsulate the idea of a Post about a Profile'''

    # data attributes for the Post:
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    caption = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this Post.'''
        return f'{self.caption}'    
