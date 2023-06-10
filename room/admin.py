from django.contrib import admin
from .models import Room, User, Book


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type')
    readonly_fields = ('date_created',)


class BookAdmin(admin.ModelAdmin):
    date_hierarchy = 'start'
    readonly_fields = ('date_created',)


admin.site.register(User)
admin.site.register(Book, BookAdmin)
