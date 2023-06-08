from datetime import datetime
from django.db import models

TYPE = (
    ('none', 'None'),
    ('focus', 'Focus'),
    ('team', 'Team'),
    ('conference', 'Conference')
)


class Room(models.Model):
    name = models.CharField(max_length=223, null=True)
    type = models.CharField(choices=TYPE, max_length=223, default='none')
    capacity = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class User(models.Model):
    name = models.CharField(max_length=223, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    resident = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, related_name='times')
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'The {self.room} room was booked {self.start.strftime("%Y-%m-%d %H:%M:%S")} - {self.end.strftime("%Y-%m-%d %H:%M:%S")}'
