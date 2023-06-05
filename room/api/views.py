from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from room.models import Room, User, Book
from .filters import RoomFilter
from .serializers import RoomSerializer, RoomBookingSerializer, BookSerializer


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
        serializer = BookSerializer(times, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)


class RoomBookingAPIView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = RoomBookingSerializer

    def create(self, request, *args, **kwargs):
        room_id = self.kwargs['pk']
        name = request.data.get('resident')['name']
        start = request.data.get('start')
        end = request.data.get('end')
        c = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
        d = datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
        print(self.get_queryset().filter(room_id=room_id).count())

        if self.get_queryset().filter(room_id=room_id).count() > 0:

            for query in self.get_queryset().filter(room_id=room_id):

                db_start = query.start
                db_end = query.end
                a = datetime.strptime(db_start, '%Y-%m-%d %H:%M:%S')
                b = datetime.strptime(db_end, '%Y-%m-%d %H:%M:%S')

                if (c < a and d <= a) or (b <= c and b < d):
                    resident = User.objects.create(name=name)
                    Book.objects.create(room_id=room_id, resident=resident, start=start, end=end)
                    return Response({"message": "xona muvaffaqiyatli band qilindi"}, status=status.HTTP_201_CREATED)
        else:
            resident = User.objects.create(name=name)
            Book.objects.create(room_id=room_id, resident=resident, start=start, end=end)
            return Response({"message": "xona muvaffaqiyatli band qilindi"}, status=status.HTTP_201_CREATED)
        return Response({"error": "uzr, siz tanlagan vaqtda xona band"}, status=status.HTTP_410_GONE)
