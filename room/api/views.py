from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from room.models import Room, User, Book
from .filters import RoomFilter, RoomAvailabilityFilter
from .serializers import RoomSerializer, RoomBookingSerializer, RoomAvailabilitySerializer


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100


class RoomListView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    pagination_class = LargeResultsSetPagination
    filterset_class = RoomFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]


@api_view(['GET'])
def room_detail(request, pk):
    try:
        room = get_object_or_404(Room, id=pk)
        serializer = RoomSerializer(room, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": "topilmadi"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def availability(request, pk):
    try:
        times = Book.objects.filter(room_id=pk)
        serializer = RoomAvailabilitySerializer(times, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)


class RoomAvailabilityRetrieveView(generics.ListAPIView):
    serializer_class = RoomAvailabilitySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = RoomAvailabilityFilter

    def get_queryset(self):
        room_id = self.kwargs['pk']
        queryset = Book.objects.filter(room_id=room_id, start__day=datetime.now().day)
        return queryset


class RoomBookingAPIView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = RoomBookingSerializer

    def create(self, request, *args, **kwargs):
        room_id = self.kwargs['pk']
        name = request.data.get('resident')['name']
        start = request.data.get('start')
        end = request.data.get('end')
        c = start
        d = end
        if self.get_queryset().filter(room_id=room_id).count() > 0:
            result = True
            for query in self.get_queryset().filter(room_id=room_id):
                if result:
                    a = query.start.strftime("%Y-%m-%d %H:%M:%S")
                    b = query.end.strftime("%Y-%m-%d %H:%M:%S")
                    if (c < a and d <= a) or (b <= c and b < d):
                        result = True
                    else:
                        result = False
            if result:
                resident = User.objects.create(name=name)
                Book.objects.create(room_id=room_id, resident=resident, start=start, end=end)
                return Response({"message": "xona muvaffaqiyatli band qilindi"}, status=status.HTTP_201_CREATED)

        else:
            resident = User.objects.create(name=name)
            Book.objects.create(room_id=room_id, resident=resident, start=start, end=end)
            return Response({"message": "xona muvaffaqiyatli band qilindi"}, status=status.HTTP_201_CREATED)
        return Response({"error": f"uzr, siz tanlagan vaqtda xona band"},
                        status=status.HTTP_410_GONE)
