from django.shortcuts import render

from .models import *
# Create your views here.

def refresh_event(event_group, player):
    return Event.objects.filter(event_group=event_group).filter(sub_order=player.current_sub_process).first()
def refresh_event_group(player):
    return EventGroup.objects.filter(order=player.current_process).first()

def my_item(player):
    print('hello')
    print (CharacterItem.objects.filter(character=player))
    return CharacterItem.objects.filter(character=player).first()

def display(request):
    
    player = Character.objects.get(is_player=1)

    event_group = refresh_event_group(player)

    event = refresh_event(event_group, player)

    character_item = CharacterItem.objects.filter(character=player).first()

    items = []

    my_items = character_item.item.all()

    for i in range(player.max_item):
        print(i)
        if i >= len(my_items.values()):
            items.append({})
        else:
            items.append(my_items.values()[i])
    

    if request.method == "POST":
        data = request.POST
        action = data.get('next')
        if action == 'next':
            if Event.objects.filter(sub_order= player.current_sub_process + 1):
                player.current_sub_process = player.current_sub_process + 1
            else:
                player.current_sub_process = 1
                player.current_process = player.current_process + 1
        player.save()
        event_group = refresh_event_group(player)
        event = refresh_event(event_group, player)

    return render(request, 'msg-box.html', {
    "player" : player,
    "event": event,
    "items": items})


def choice(request):

    pass


def my_item(request):

    pass