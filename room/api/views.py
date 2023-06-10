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
            curr_time = datetime.strptime(curr_time, '%Y-%m-%d')

        queryset = Book.objects.filter(
            Q(room_id=room_id),
            Q(Q(start__day=curr_time.day) | Q(end__day=curr_time.day))
        ).order_by('start')

        room = Room.objects.get(id=room_id)
        booked_list = []

        for booked in queryset:

            start = room.active_date
            end = room.inactive_date

            if booked.start.date() == curr_time.date():
                start = booked.start

            if booked.start.date() == curr_time.date():
                end = booked.end

            booked_list.append((start, end))

        availability_list = []
        previous_end = room.active_date

        for start, end in booked_list:

            if previous_end < start.time():
                availability_list.append({
                    "start": f"{curr_time.date()} {previous_end}",
                    "end": f"{curr_time.date()} {start.time()}"
                })

            previous_end = end.time()

        if previous_end < room.inactive_date:
            availability_list.append({
                "start": f"{curr_time.date()} {previous_end}",
                "end": f"{curr_time.date()} {room.inactive_date}"
            })

        return availability_list


class RoomBookingAPIView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = RoomBookingSerializer

    def create(self, request, *args, **kwargs):
        try:
            room_id = self.kwargs['pk']
            name = request.data.get('resident')['name']  # user's name
            start = request.data.get('start')  # time comes in str format
            end = request.data.get('end')  # time comes in str format
            c = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
            # -> 2023-06-10 12:00:00+00:00  str is formatted to time
            d = datetime.strptime(end, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)

            obj_room = Room.objects.get(id=room_id)
            db_act = obj_room.active_date
            db_inact = obj_room.inactive_date

            if self.get_queryset().filter(room_id=room_id).count() > 0:  # more than once
                result = True
                for query in self.get_queryset().filter(room_id=room_id):
                    if result:
                        a = query.start  # -> 2023-06-10 12:00:00+00:00
                        b = query.end  # .strftime("%Y-%m-%d %H:%M")

                        if (c < a and d <= a) or (b <= c and b < d):
                            result = True
                        else:
                            result = False
                            conflict_time2 = b - c

                if result:
                    resident = User.objects.create(name=name)
                    Book.objects.create(room_id=room_id, resident=resident, start=start, end=end)
                    return Response({"message": "xona muvaffaqiyatli band qilindi"}, status=status.HTTP_201_CREATED)

            else:  # first time
                resident = User.objects.create(name=name)
                Book.objects.create(room_id=room_id, resident=resident, start=start, end=end)
                return Response({"message": "xona muvaffaqiyatli band qilindi"}, status=status.HTTP_201_CREATED)
            return Response({
                "error": f"Uzr, siz tanlagan vaqtda xona band.",
                "message": f"Eslatib o'tamizki xona {db_act} - {db_inact} ochiq bo'ladi."
            }, status=status.HTTP_410_GONE)

        except Exception as e:
            return Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)
