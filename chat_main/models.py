from django.db import models
from datetime import datetime

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):  # Отображает name в админке
        return self.name

class Msg(models.Model):
    value = models.CharField(max_length=10000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    send = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    user = models.CharField(max_length=128)
    room = models.CharField(max_length=128)

    def __str__(self):  # Отображает value в админке
        return self.value