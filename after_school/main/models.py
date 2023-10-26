from django.db import models

# Create your models here.
class Character(models.Model):

    name = models.CharField(max_length=200)
    hp = models.FloatField(default=0)
    attack = models.FloatField(default=0)
    is_player = models.BooleanField(default=False)
    current_process = models.IntegerField(default=1)
    current_sub_process = models.IntegerField(default=1)

    def __str__(self):
        return self.name



class EventGroup(models.Model):
    EVENT_CHOICE = [
        ('S', 'Speech'),
        ('B', 'Battle'),
    ]

    name = models.CharField(max_length=200)
    type = models.CharField(max_length=1, choices=EVENT_CHOICE)
    order = models.IntegerField()

    def __str__(self):
        return self.name

class Event(models.Model):
    
    event_group = models.ForeignKey(EventGroup, on_delete=models.CASCADE)
    text = models.TextField()
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    sub_order = models.IntegerField()

    def __str__(self):
        return str(self.event_group)+ ' | ' + str(self.text) + ' | ' + str(self.sub_order)