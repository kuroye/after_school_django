from django.shortcuts import render, redirect
from django.urls import reverse

from .models import *
# Create your views here.

def refresh_event(event_group, player):
    return Event.objects.filter(event_group=event_group).filter(sub_order=player.current_sub_process).first()
def refresh_event_group(player):
    return EventGroup.objects.filter(order=player.current_process).first()

def refresh_process(player):
    event_group = refresh_event_group(player)
    event = refresh_event(event_group, player)
    return event_group, event

def get_choices(event_group):
    return Choice.objects.filter(event__event_group=event_group)
def restart(player):
    player.current_sub_process = 0
    player.current_process = 0

def my_item(player):
    print('hello')
    print (CharacterItem.objects.filter(character=player))
    return CharacterItem.objects.filter(character=player).first()

def display(request):
    

    

    player = Character.objects.get(is_player=1)

    if not EventGroup.objects.filter(order=player.current_process):
        player.current_sub_process = 0
        player.current_process = 0
        

    event_group = refresh_event_group(player)

    event = refresh_event(event_group, player)

    character_item = CharacterItem.objects.filter(character=player).first()

    items = []

    my_items = character_item.item.all()

    for i in range(player.max_item):
        if i >= len(my_items.values()):
            items.append({})
        else:
            items.append(my_items.values()[i])
    



    


    if request.method == "POST":
        data = request.POST
        action = data.get('action')

        print(action)

        if action == 'restart':
            player.current_sub_process = 0
            player.current_process = 0

            player.save()
            event_group, event = refresh_process(player)
            
            return redirect(reverse('main'))
        if action == 'next':
            if Event.objects.filter(event_group__order=player.current_process).filter(sub_order= player.current_sub_process + 1):
                print(Event.objects.filter(sub_order= player.current_sub_process + 1))
                player.current_sub_process = player.current_sub_process + 1
                
                print(player.current_process)
                print(player.current_sub_process)
                print('------')

                player.save()
                event_group, event = refresh_process(player)

                return redirect(reverse('main'))
            else:
                player.current_sub_process = 1
                player.current_process = player.current_process + 1

                player.save()
                event_group, event = refresh_process(player)

                return redirect(reverse('main'))

        if 'choices' in action or 'next-with-jump-to' in action:
            jump_to = str.split(action,'|')[1]
            player.current_sub_process = 1
            player.current_process = int(jump_to)

            player.save()
            event_group, event = refresh_process(player)

            return redirect(reverse('main'))
                
        player.save()
        event_group, event = refresh_process(player)


    context = {
        "player" : player,
        "event": event,
        "items": items
        }

    if event_group.type == 'C':
        context['choices'] = get_choices(event_group)
        return render(request, 'choices.html', context)
    else:
        return render(request, 'msg-box.html', context)


def choice(request):

    pass

