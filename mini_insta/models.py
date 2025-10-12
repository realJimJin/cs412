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
    def get_all_posts(self):
        '''Return a QuerySet of posts about this article.'''
        # use the object manager to retrieve posts about this profile
        posts = Post.objects.filter(profile=self)
        return posts

class Post(models.Model):
    '''Encapsulate the idea of a Post about a Profile'''

    # data attributes for the Post:
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    caption = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now=True)

    def get_all_photos(self):
        '''Return a QuerySet of photos about this post.'''
        # use the object manager to retrieve photos about this post
        photos = Photo.objects.filter(post=self)
        return photos

    def __str__(self):
        '''Return a string representation of this Post.'''
        return f'{self.caption}'


class Photo(models.Model):
    '''Encapsulate the idea of a Photo about a Post'''

    # data attributes for the Photo:
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_file = models.ImageField(blank=True) # an actual image
    image_url = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def get_image_url(self):
        '''Return the url of the image_file or image_url if there is one'''
        if self.image_url is not None:
            return self.image_url 
        return self.image_file.url 

    def __str__(self):
        '''Return a string representation of this Photo.'''
        return f'{self.get_image_url()}'    
