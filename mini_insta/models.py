from django.db import models
from django.urls import reverse

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
    def get_absolute_url(self):
        # Redirect back to this profile’s page after successful update
        return reverse("mini_insta:show_profile", kwargs={"pk": self.pk})
    def get_followers(self):
        """
        Return a list of Profile objects that follow this profile.
        i.e., all follower_profile where profile == self
        """
        followers_qs = Profile.objects.filter(follower_profile__profile=self).distinct()
        return list(followers_qs)

    def get_num_followers(self):
        """
        Return the count of followers for this profile.
        """
        return Follow.objects.filter(profile=self).count()

    def get_following(self):
        """
        Return a list of Profile objects that this profile is following.
        i.e., all profile where follower_profile == self
        """
        following_qs = Profile.objects.filter(profile__follower_profile=self).distinct()
        return list(following_qs)

    def get_num_following(self):
        """
        Return the count of profiles this profile is following.
        """
        return Follow.objects.filter(follower_profile=self).count()

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

    def get_all_comments(self):
        """Return all comments for this post (newest first)."""
        return Comment.objects.filter(post=self).select_related("profile").order_by("-timestamp")

    def __str__(self):
        '''Return a string representation of this Post.'''
        return f'{self.caption}'


class Photo(models.Model):
    """Encapsulate the idea of a Photo about a Post"""

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_file = models.ImageField(blank=True)
    image_url = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def get_image_url(self):
        """
        Prefer uploaded file if present; otherwise fall back to the image_url.
        """
        if self.image_url:
            return self.image_url

        return self.image_file.url


    def __str__(self):
        return f'{self.get_image_url()}'


class Follow(models.Model):
    '''Encapsulates the idea of a Follow between one profile and another'''

    #data attributes for the Follow:
    profile= models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile')
    follower_profile=models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='follower_profile')
    timestamp=  models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.timestamp}'


class Comment(models.Model):
    """A comment made by a Profile on a Post."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        preview = (self.text[:40] + "…") if len(self.text) > 40 else self.text
        return f"@{self.profile.username} on Post#{self.post.pk} — {preview}"

class Like(models.Model):
    """A 'like' made by a Profile on a Post."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="likes")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Prevent duplicate likes by the same profile on the same post
        constraints = [
            models.UniqueConstraint(fields=["post", "profile"], name="unique_like_per_profile_per_post")
        ]

    def __str__(self):
        return f"Like by @{self.profile.username} on Post#{self.post.pk} at {self.timestamp}"           
