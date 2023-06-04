from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from room.models import Room, FreeTime, Book
from .serializers import RoomSerializer, FreeTimeSerializer, FreeTimeBookSerializer, BookSerializer


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100


class RoomListView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    pagination_class = LargeResultsSetPagination


@api_view(['GET'])
def room_detail(request, pk):
    try:
        room = get_object_or_404(Room, id=pk)
        serializer = RoomSerializer(room, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": "topilmadi"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def availability(request, pk):
    try:
        times = FreeTime.objects.filter(room_id=pk)
        serializer = FreeTimeSerializer(times, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)


# class BookAPIView(generics.CreateAPIView):
#     queryset = FreeTime.objects.all()
#     serializer_class = FreeTimeBookSerializer

@api_view(["POST"])
def book_create(request, pk):
    try:
        sz = FreeTimeBookSerializer(data=request.data)
        name = request.data.get('resident')['name']
        resident = Book.objects.create(name=name)
        FreeTime.objects.create(room_id=pk, resident=resident)
        if sz.is_valid(raise_exception=True):
            sz.save()
            return Response({"message": "xona muvaffaqiyatli band qilindi"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": f"{e}"})


    # resident = request.data.get('resident')['name']
    # book = Book.objects.create(name=resident)
    # start = request.data.get('start')
    # end = request.data.get('end')
    # qs = FreeTime.objects.create(room_id=pk, resident=book, start=start, end=end)
    # return Response({"message": "xona muvaffaqiyatli band qilindi"}, status=status.HTTP_201_CREATED)