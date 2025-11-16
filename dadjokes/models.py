import random
from django.shortcuts import render, get_object_or_404
from .models import Joke, Picture

def random_view(request):
    joke = random.choice(Joke.objects.all())
    picture = random.choice(Picture.objects.all())
    return render(request, 'dadjokes/random.html', {
        'joke': joke,
        'picture': picture,
    })

def jokes_list(request):
    jokes = Joke.objects.all().order_by('-created_at')
    return render(request, 'dadjokes/jokes_list.html', {'jokes': jokes})

def joke_detail(request, pk):
    joke = get_object_or_404(Joke, pk=pk)
    return render(request, 'dadjokes/joke_detail.html', {'joke': joke})

def pictures_list(request):
    pictures = Picture.objects.all().order_by('-created_at')
    return render(request, 'dadjokes/pictures_list.html', {'pictures': pictures})

def picture_detail(request, pk):
    picture = get_object_or_404(Picture, pk=pk)
    return render(request, 'dadjokes/picture_detail.html', {'picture': picture})
