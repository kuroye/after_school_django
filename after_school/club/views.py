from django.shortcuts import render,redirect
from main.models import *
from django.urls import reverse

# Create your views here.

def display(request):
    player = Character.objects.get(is_player=1)

    character_item = CharacterItem.objects.filter(character=player).first()

    items = []

    my_items = character_item.item.all()

    for i in range(player.max_item):
        if i >= len(my_items.values()):
            items.append({})
        else:
            items.append(my_items.values()[i])


    club = player.club
    club_skills = Skill.objects.filter(club=club)

    if request.method == "POST":
        data = request.POST
        action = data.get('action')

        if 'buy-skill' in action:
            skill_name = str.split(action,'|')[1]
            Skill.objects.filter(name=skill_name).update(user=player,is_purchased=True)
            
            return redirect((reverse('club')))

    context = {
        "player" : player,
        "items": items,
        "skills": club_skills,
        }

    return render(request, 'club.html', context)
    