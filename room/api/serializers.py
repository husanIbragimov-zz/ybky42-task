from rest_framework import serializers
from room.models import FreeTime, Room, Book


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'name', 'type', 'capacity')


class FreeTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreeTime
        fields = ('start', 'end')


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('name',)


class FreeTimeBookSerializer(serializers.ModelSerializer):
    resident = BookSerializer(write_only=True)

    class Meta:
        model = FreeTime
        fields = ('resident', 'start', 'end')

    def create(self, validated_data):

        return "OK"
