from django.urls import path
from .views import RoomListCreateView, room_detail, RoomAvailabilityRetrieveView, RoomBookingAPIView, \
    RoomNotAvailableListView

urlpatterns = [
    path('rooms/', RoomListCreateView.as_view()),
    path('rooms/<int:pk>/', room_detail),
    path('rooms/<int:pk>/availability/', RoomAvailabilityRetrieveView.as_view()),
    path('rooms/<int:pk>/book/', RoomBookingAPIView.as_view()),

    path('rooms/<int:pk>/not-available/', RoomNotAvailableListView.as_view()),
]
