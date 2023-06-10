from django.contrib import admin
from .models import Room, User, Book


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type')


class BookAdmin(admin.ModelAdmin):
    date_hierarchy = 'start'


admin.site.register(User)
admin.site.register(Book, BookAdmin)
