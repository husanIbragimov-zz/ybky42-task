from django.contrib import admin
from .models import Room, User, Book


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type')


admin.site.register(User)
admin.site.register(Book)
