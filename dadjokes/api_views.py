import random
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Joke, Picture
from .serializers import JokeSerializer, PictureSerializer


@api_view(['GET'])
def random_joke(request):
    jokes = Joke.objects.all()
    if not jokes:
        return Response({'detail': 'no jokes'}, status=status.HTTP_404_NOT_FOUND)
    joke = random.choice(list(jokes))
    return Response(JokeSerializer(joke).data)


@api_view(['GET', 'POST'])
def jokes_list(request):
    if request.method == 'GET':
        jokes = Joke.objects.all().order_by('-created_at')
        serializer = JokeSerializer(jokes, many=True)
        return Response(serializer.data)

    # POST: create new Joke
    serializer = JokeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def joke_detail(request, pk):
    try:
        joke = Joke.objects.get(pk=pk)
    except Joke.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = JokeSerializer(joke)
    return Response(serializer.data)


@api_view(['GET'])
def pictures_list(request):
    pictures = Picture.objects.all().order_by('-created_at')
    serializer = PictureSerializer(pictures, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def picture_detail(request, pk):
    try:
        picture = Picture.objects.get(pk=pk)
    except Picture.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = PictureSerializer(picture)
    return Response(serializer.data)


@api_view(['GET'])
def random_picture(request):
    pictures = Picture.objects.all()
    if not pictures:
        return Response({'detail': 'no pictures'}, status=status.HTTP_404_NOT_FOUND)
    picture = random.choice(list(pictures))
    return Response(PictureSerializer(picture).data)
