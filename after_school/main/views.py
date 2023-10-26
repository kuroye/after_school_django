from django.shortcuts import render

from .models import Character, Event, EventGroup
# Create your views here.

def refresh_event(event_group, player):
    return Event.objects.filter(event_group=event_group).filter(sub_order=player.current_sub_process).first()
def refresh_event_group(player):
    return EventGroup.objects.filter(order=player.current_process).first()

def display(request):
    
    player = Character.objects.get(is_player=1)

    event_group = refresh_event_group(player)

    event = refresh_event(event_group, player)

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

    return render(request, 'main.html', {
    "player" : player,
    "event": event})

