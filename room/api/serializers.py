from rest_framework import serializers
from room.models import Book, Room, User


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'name', 'type', 'capacity')


class RoomAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('start', 'end')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name',)


class RoomNotAvailabilitySerializer(serializers.ModelSerializer):
    resident = UserSerializer(read_only=True)

    class Meta:
        model = Book
        fields = ('resident', 'start', 'end')


class RoomBookingSerializer(serializers.ModelSerializer):
    resident = UserSerializer(write_only=True)

    class Meta:
        model = Book
        fields = ('resident', 'start', 'end')
