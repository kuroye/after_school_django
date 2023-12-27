from django.db import models
from club.models import Club
# Create your models here.
class Character(models.Model):

    name = models.CharField(max_length=200)
    max_hp = models.FloatField(default=0)
    current_hp = models.FloatField(default=0)
    attack = models.FloatField(default=0)
    is_player = models.BooleanField(default=False)
    current_process = models.IntegerField(default=1)
    current_sub_process = models.IntegerField(default=1)

    max_item = models.IntegerField(default=3)

    club = models.ForeignKey(Club, on_delete=models.CASCADE, null=True, blank=True, related_name='club')

    def __str__(self):
        return self.name


def find_last_group():
    last_group = EventGroup.objects.all().order_by('order').last()
    return last_group.order+1

class EventGroup(models.Model):
    EVENT_CHOICE = [
        ('S', 'Speech'),
        ('B', 'Battle'),
        ('C', 'Choice'),
    ]

    name = models.CharField(max_length=200)
    type = models.CharField(max_length=1, choices=EVENT_CHOICE)
    order = models.IntegerField(default=find_last_group)

    def __str__(self):
        return str(self.type)+ ' | ' +str(self.name) +' | '+ str(self.order)


def find_last_order():
    last_group = Event.objects.all().order_by('event_group').last().event_group
    return last_group
def find_last_sub_order():
    last_group = Event.objects.all().order_by('event_group').last().event_group
    last_sub_order = Event.objects.filter(event_group=last_group).order_by('sub_order').last()
    return last_sub_order.sub_order+1

class Event(models.Model):

    event_group = models.ForeignKey(EventGroup, on_delete=models.CASCADE, default=find_last_order)
    text = models.TextField()
    character = models.ForeignKey(Character, on_delete=models.CASCADE, blank=True, null=True)
    sub_order = models.IntegerField(default=find_last_sub_order)
    jump_to = models.ForeignKey(EventGroup, on_delete=models.CASCADE, null=True, blank=True, related_name='jump_to_from_event')

    p2 = models.ForeignKey(Character, on_delete=models.CASCADE, blank=True, null=True, related_name='p2')
    round = models.IntegerField(default=1)
    p2_act = models.BooleanField(default=False)
    victory = models.ForeignKey(EventGroup, on_delete=models.CASCADE, null=True, blank=True, related_name='jump_to_if_victory')
    lose = models.ForeignKey(EventGroup, on_delete=models.CASCADE, null=True, blank=True, related_name='jump_to_if_lose')
    finish = models.BooleanField(default=False, null=True)

    def __str__(self):
        return str(self.event_group)+ ' > ' + str(self.text) + ' | ' + str(self.sub_order)


class Choice(models.Model):

    name = models.CharField(max_length=200)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    jump_to = models.ForeignKey(EventGroup, on_delete=models.CASCADE, null=True, blank=True, related_name='jump_to_from_choice')
    club = models.ForeignKey(Club, on_delete=models.CASCADE, null=True, blank=True, related_name='club_choice')

    def __str__(self):
        return str(self.event) +' | '+ str(self.name)

class Battle(models.Model):

    name = models.CharField(max_length=200)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    jump_to = models.ForeignKey(EventGroup, on_delete=models.CASCADE, null=True, blank=True, related_name='jump_to_from_battle')

    def __str__(self):
        return str(self.event.event_group.name) +' | '+ str(self.name)

class Skill(models.Model):

    name = models.CharField(max_length=200)
    min_atk = models.IntegerField(default=0)
    max_atk = models.IntegerField(default=0)

    user = models.ForeignKey(Character, on_delete=models.CASCADE, blank=True, null=True)

    audio = models.FileField(upload_to='audio/skill/',null=True, blank=True)
    def __str__(self):
        return str(self.name)

class Item(models.Model):

    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/item_images/',null=True, blank=True)
    attack = models.FloatField(default=0)

    def __str__(self):
        return self.name

class CharacterItem(models.Model):

    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    item = models.ManyToManyField(Item, null=True, blank=True)

    def __str__(self):
        return str(self.character) + '的背包'


class Video(models.Model):

    name = models.CharField(max_length=200)
    video = models.FileField(upload_to='videos/', null=True)

    def __str__(self):
        return str(self.name)