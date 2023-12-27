from django.shortcuts import render
from main.models import *

# Create your views here.

def display(request):
    player = Character.objects.get(is_player=1)

    context = {
        "player" : player,
        }

    return render(request, 'club.html', context)
    