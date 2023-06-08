from datetime import datetime
from django.db.models import Q
from .filters import RoomFilter
from django.utils import timezone
from room.models import Room, User, Book
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import RoomSerializer, RoomBookingSerializer, RoomAvailabilitySerializer


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100


class RoomListView(generics.ListCreateAPIView):
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


class RoomAvailabilityRetrieveView(generics.ListAPIView):
    serializer_class = RoomAvailabilitySerializer

    def get_queryset(self):
        room_id = self.kwargs['pk']
        curr_time = self.request.GET.get('date', datetime.now(timezone.utc))
        if isinstance(curr_time, str):
            curr_time = datetime.strptime(curr_time, '%Y-%m-%d').replace(tzinfo=timezone.utc)
        queryset = Book.objects.filter(
            Q(room_id=room_id),
            Q(Q(start__day=curr_time.day) | Q(end__day=curr_time.day))
        ).order_by('start')

        booked_list = []
        for booked in queryset:
            start = curr_time.replace(hour=00, minute=00, second=00)
            end = curr_time.replace(hour=23, minute=59, second=59)
            print(booked.start.date())
            if booked.start.date() == curr_time.date():
                start = booked.start

            if booked.start.date() == curr_time.date():
                end = booked.end
            booked_list.append((start, end))

        availability_list = []
        previous_end = curr_time.replace(hour=00, minute=00, second=00)
        for start, end in booked_list:
            if previous_end < start:
                availability_list.append({
                    "start": str(previous_end),
                    "end": str(start)
                })
            previous_end = end
        if previous_end < curr_time.replace(hour=23, minute=59, second=59):
            availability_list.append({
                "start": str(previous_end),
                "end": str(curr_time.replace(hour=23, minute=59, second=59))
            })

        return availability_list


class RoomBookingAPIView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = RoomBookingSerializer

    def create(self, request, *args, **kwargs):
        room_id = self.kwargs['pk']
        name = request.data.get('resident')['name']
        start = request.data.get('start')
        end = request.data.get('end')
        print(start)
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
