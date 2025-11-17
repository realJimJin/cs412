from django.shortcuts import render, get_object_or_404
import random

from .models import Joke, Picture


def random_view(request):
    """Show one random Joke and one random Picture."""
    jokes = Joke.objects.all()
    pictures = Picture.objects.all()

    joke = random.choice(list(jokes)) if jokes else None
    picture = random.choice(list(pictures)) if pictures else None

    return render(request, 'dadjokes/random.html', {
        'joke': joke,
        'picture': picture,
    })


def jokes_list(request):
    """Show a page with all Jokes (no images)."""
    jokes = Joke.objects.all().order_by('-created_at')
    return render(request, 'dadjokes/jokes_list.html', {'jokes': jokes})


def joke_detail(request, pk):
    """Show one Joke by its primary key."""
    joke = get_object_or_404(Joke, pk=pk)
    return render(request, 'dadjokes/joke_detail.html', {'joke': joke})


def pictures_list(request):
    """Show a page with all Pictures (no jokes)."""
    pictures = Picture.objects.all().order_by('-created_at')
    return render(request, 'dadjokes/pictures_list.html', {'pictures': pictures})


def picture_detail(request, pk):
    """Show one Picture by its primary key."""
    picture = get_object_or_404(Picture, pk=pk)
    return render(request, 'dadjokes/picture_detail.html', {'picture': picture})
