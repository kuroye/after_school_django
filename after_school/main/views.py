from django.shortcuts import render, redirect
from django.urls import reverse

from .models import *

import random
from pygame import mixer

import os
from django.conf import settings

import time
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
    


    player.save()
    event_group, event = refresh_process(player)
    


    if request.method == "POST":
        data = request.POST
        action = data.get('action')

        print(action)
        # print(event.event_group.type)

        if action == 'restart':
            # player.current_sub_process = 0
            player.current_sub_process = 1
            # player.current_process = 0
            player.current_process = 7
            player.current_hp = 100

            player.save()
            event_group, event = refresh_process(player)
            
            return redirect(reverse('main'))
        if action == 'next' and event.event_group.type != 'B':
            print('是不是')
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
            if 'club' in action:
                club_name = str.split(action,'|')[2]
                club = Club.objects.filter(name=club_name).first()
                player.club = club
            
            jump_to = str.split(action,'|')[1]
            player.current_sub_process = 1
            player.current_process = int(jump_to)

            player.save()
            event_group, event = refresh_process(player)

            return redirect(reverse('main'))
        
        
        if event.event_group.type == 'B':
            # 我的回合，当我出招后
            if 'battle' in action:

                skill = str.split(action,'|')
                skill_name = skill[1]
                skill_min_atk = int(skill[2])
                skill_max_atk = int(skill[3])
                skill_audio = skill[4]
                damage = random.randint(skill_min_atk,skill_max_atk)
                enemy = event.p2
                enemy.current_hp = enemy.current_hp - damage

                battle_info = str(player.name) + '使出了' + str(skill_name) + ', 对' + str(enemy.name) + '造成了' + str(damage) + '点伤害'
                print(skill_audio)
                normalized_path = os.path.normpath(skill_audio)
                print(normalized_path)
                full_path_audio = os.path.join(settings.MEDIA_ROOT, normalized_path)
                print(full_path_audio)
                mixer.init()
                mixer.music.load(full_path_audio)
                mixer.music.play()
                time.sleep(1.5)
                event.round = event.round + 1
                event.p2_act = False
                event.save()
                enemy.save()
                Battle.objects.create(name=battle_info,event=event)
                return redirect(reverse('main'))
            
            else:
                # 对手的回合
                print('YEES,LOOK')
                enemy = event.p2
                
                if event.p2_act:
                    event.round = event.round + 1
                else:

                    skills = Skill.objects.filter(user=enemy)
                    skill = random.choice(skills)
                    skill_name = skill.name
                    skill_min_atk = int(skill.min_atk)
                    skill_max_atk = int(skill.max_atk)
                    skill_audio = skill.audio
                    damage = random.randint(skill_min_atk,skill_max_atk)
                    player.current_hp = player.current_hp - damage
                    player.save()
                    normalized_path = os.path.normpath(skill_audio.path)
                    print(normalized_path)
                    full_path_audio = os.path.join(settings.MEDIA_ROOT, normalized_path)
                    print(full_path_audio)
                    mixer.init()
                    mixer.music.load(full_path_audio)
                    mixer.music.play()
                    # time.sleep(1.5)
                

                    battle_info = str(enemy.name) + '使出了' + str(skill_name) + ', 对' + str(player.name) + '造成了' + str(damage) + '点伤害'
                    Battle.objects.create(name=battle_info,event=event)
                    event.p2_act = True

                event.save()
                return redirect(reverse('main'))


    context = {
        "player" : player,
        "event": event,
        "items": items
        }

    if event_group.type == 'C':
        context['choices'] = get_choices(event_group)
        return render(request, 'choices.html', context)
    elif event_group.type == 'B':

        if event.p2.current_hp <= 0:
            if event.finish:
                jump_to = event.victory.order
                player.current_sub_process = 1
                player.current_process = int(jump_to)

                player.save()
                event_group, event = refresh_process(player)

                return redirect(reverse('main'))
            else:
                context['event'].text = "恭喜你战胜了" + str(event.p2.name)
                context['enemy'] = event.p2
                context['event'].event_group.type = 'S'
                Event.objects.filter(pk=event.pk).update(finish=True)

            
                return render(request, 'battle.html', context)

        if player.current_hp <= 0:
            if event.finish:
                jump_to = event.lose.order
                player.current_sub_process = 1
                player.current_process = int(jump_to)

                player.save()
                event_group, event = refresh_process(player)

                return redirect(reverse('main'))
            else:
                context['enemy'] = event.p2
                context['event'].text = "很可惜你失败了"
                context['event'].event_group.type = 'S'
                Event.objects.filter(pk=event.pk).update(finish=True)
                return render(request, 'battle.html', context)


        if event.round%2!=0 and event.p2_act is False:
            if event.round ==1:
                print("I AM 1")
                context['event'].text = event.text
            else:
                print("I AM 1.5")
                context['event'].text = Battle.objects.all().last().name 

            
            context['skills'] = Skill.objects.filter(user=player)
            context['enemy'] = event.p2
            return render(request, 'battle.html', context)

        elif event.p2_act and event.round%2!=0:
            print("I AM 2")

            context['enemy'] = event.p2
            context['skills'] = Skill.objects.filter(user=player)
            context['event'].text = "你的选择是:"
            return render(request, 'battle.html', context)

        else:
            print("I AM 3")

            context['enemy'] = event.p2
            context['event'].text = Battle.objects.all().last().name
            return render(request, 'battle.html', context)
    else:
        return render(request, 'msg-box.html', context)
        


def choice(request):

    pass

