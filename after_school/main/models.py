from django.db import models

# Create your models here.
class Character(models.Model):

    name = models.CharField(max_length=200)
    hp = models.FloatField(default=0)
    attack = models.FloatField(default=0)
    is_player = models.BooleanField(default=False)
    current_process = models.IntegerField(default=1)
    current_sub_process = models.IntegerField(default=1)

    max_item = models.IntegerField(default=3)

    def __str__(self):
        return self.name



class EventGroup(models.Model):
    EVENT_CHOICE = [
        ('S', 'Speech'),
        ('B', 'Battle'),
        ('C', 'Choice'),
    ]

    name = models.CharField(max_length=200)
    type = models.CharField(max_length=1, choices=EVENT_CHOICE)
    order = models.IntegerField()

    def __str__(self):
        return self.name


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


    def __str__(self):
        return str(self.event_group)+ ' | ' + str(self.text) + ' | ' + str(self.sub_order)




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