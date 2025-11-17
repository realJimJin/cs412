from django.db import models


class Joke(models.Model):
    text = models.TextField()
    contributor = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.text[:40]}... by {self.contributor}'


class Picture(models.Model):
    image_url = models.URLField()
    contributor = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Picture by {self.contributor}'
