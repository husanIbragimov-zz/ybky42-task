from datetime import datetime
from django.db.models import Q
from .filters import RoomFilter
from room.models import Room, User, Book
from typing_extensions import OrderedDict
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import RoomSerializer, RoomBookingSerializer, RoomAvailabilitySerializer, \
    RoomNotAvailabilitySerializer


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('page', self.page.number),
            ('page_size', self.page_size),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))


class RoomListCreateView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    search_fields = ['name', 'type']
    filterset_class = RoomFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    pagination_class = LargeResultsSetPagination


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
        curr_time = self.request.GET.get('date', datetime.now().strftime("%d-%m-%Y"))
        obj_date = datetime.strptime(curr_time, '%d-%m-%Y')
        cur = obj_date.strftime("%Y-%m-%d")
        cur_date = datetime.strptime(cur, "%Y-%m-%d")

        queryset = Book.objects.filter(
            Q(room_id=room_id),
            Q(Q(start__day=cur_date.day) | Q(end__day=cur_date.day))
        ).order_by('start')

        room = Room.objects.get(id=room_id)
        start = room.open
        end = room.close

        booked_list = []

        for booked in queryset:
            if booked.start.date() == cur_date.date():
                start = booked.start.time()

            if booked.end.date() == cur_date.date():
                end = booked.end.time()

            booked_list.append((start, end))

        availability_list = []
        previous_end = room.open

        for start, end in booked_list:

            if previous_end < start:
                availability_list.append({
                    "start": f"{curr_time} {previous_end}",
                    "end": f"{curr_time} {start}"
                })

            previous_end = end

        if previous_end < room.close:
            availability_list.append({
                "start": f"{curr_time} {previous_end}",
                "end": f"{curr_time} {room.close}"
            })

        return availability_list


class RoomNotAvailableListView(generics.ListAPIView):
    serializer_class = RoomNotAvailabilitySerializer

    def get_queryset(self):
        room_id = self.kwargs['pk']
        curr_time = self.request.GET.get('date', datetime.now().date())

        queryset = Book.objects.filter(
            Q(room_id=room_id),
            Q(Q(start__day=curr_time.day) | Q(end__day=curr_time.day))
        ).order_by('start')

        date_list = []
        for date in queryset:
            a = date.start
            b = date.end
            date_list.append({
                "resident": date.resident,
                "start": f"{a.date()} {a.time()}",
                "end": f"{b.date()} {b.time()}"
            })

        return date_list


class RoomBookingAPIView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = RoomBookingSerializer

    def create(self, request, *args, **kwargs):
        room_id = self.kwargs['pk']
        name = request.data.get('resident')['name']  # user's name
        start = request.data.get('start')  # time comes in str format
        end = request.data.get('end')  # time comes in str format
        try:
            c = parse_time(start)
            d = parse_time(end)

            if self.get_queryset().filter(room_id=room_id).count() > 0:  # more than once
                result = True
                for query in self.get_queryset().filter(room_id=room_id):
                    if result:
                        a = query.start.strftime("%Y-%m-%d %H:%M:%S")  # -> 2023-06-10 12:00:00+00:00
                        b = query.end.strftime("%Y-%m-%d %H:%M:%S")

                        if (c < a and d <= a) or (b <= c and b < d):
                            result = True
                        else:
                            result = False

                if result:
                    resident = User.objects.create(name=name)
                    Book.objects.create(room_id=room_id, resident=resident, start=c, end=d)
                    return Response({"message": "xona muvaffaqiyatli band qilindi"}, status=status.HTTP_201_CREATED)

            else:  # first time
                resident = User.objects.create(name=name)
                Book.objects.create(room_id=room_id, resident=resident, start=c, end=d)
                return Response({"message": "xona muvaffaqiyatli band qilindi"}, status=status.HTTP_201_CREATED)
            return Response({
                "error": f"uzr, siz tanlagan vaqtda xona band"
            }, status=status.HTTP_410_GONE)

        except Exception as e:
            return Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)


def parse_time(time):
    obj_date = datetime.strptime(time, '%d-%m-%Y %H:%M:%S')
    cur = obj_date.strftime("%Y-%m-%d %H:%M:%S")
    return cur
