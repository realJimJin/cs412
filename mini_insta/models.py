from django.db import models
from django.urls import reverse
from django.db.models import Prefetch
from django.contrib.auth.models import User

class Profile(models.Model):
    """Encapsulate the data of a user profile on mini_insta."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="profiles",
        null=True,
        blank=True,
        default=1
    )
    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now=True)
    profile_image_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.username} displays as {self.display_name}"

    def get_all_posts(self):
        return Post.objects.filter(profile=self)

    def get_absolute_url(self):
        return reverse("mini_insta:show_profile", kwargs={"pk": self.pk})

    # Followers / Following
    def get_followers(self):
        followers_qs = Profile.objects.filter(follower_profile__profile=self).distinct()
        return list(followers_qs)

    def get_num_followers(self):
        return Follow.objects.filter(profile=self).count()

    def get_following(self):
        following_qs = Profile.objects.filter(profile__follower_profile=self).distinct()
        return list(following_qs)

    def get_num_following(self):
        return Follow.objects.filter(follower_profile=self).count()

    def get_post_feed(self):
        followed_ids = (
            Follow.objects.filter(follower_profile=self)
            .values_list("profile_id", flat=True)
        )
        qs = (
            Post.objects.filter(profile_id__in=followed_ids)
            .select_related("profile")
            .prefetch_related(
                Prefetch("photo_set", queryset=Photo.objects.order_by("timestamp"))
            )
            .order_by("-timestamp")
        )
        return qs


class Post(models.Model):
    """Encapsulate the idea of a Post about a Profile."""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    caption = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.caption}"

    def get_all_photos(self):
        return Photo.objects.filter(post=self)

    def get_all_comments(self):
        return Comment.objects.filter(post=self).select_related("profile").order_by("-timestamp")

    def get_likes(self):
        return Like.objects.filter(post=self).select_related("profile").order_by("-timestamp")

    def get_num_likes(self):
        return self.likes.count()


class Photo(models.Model):
    """Encapsulate the idea of a Photo about a Post."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_file = models.ImageField(blank=True, null=True)  # null for safety
    image_url = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def get_image_url(self):
        # Prefer uploaded file if present; otherwise fall back to the image_url.
        if self.image_file:
            try:
                return self.image_file.url
            except ValueError:
                # File not saved yet
                pass
        return self.image_url or ""

    def __str__(self):
        return f"{self.get_image_url()}"


class Follow(models.Model):
    """Encapsulates the idea of a Follow between one profile and another."""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile")
    follower_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="follower_profile")
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.timestamp}"


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
        constraints = [
            models.UniqueConstraint(
                fields=["post", "profile"],
                name="unique_like_per_profile_per_post",
            )
        ]

    def __str__(self):
        return f"Like by @{self.profile.username} on Post#{self.post.pk} at {self.timestamp}"
