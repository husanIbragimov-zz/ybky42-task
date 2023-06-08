from django.urls import path
from .views import RoomListView, room_detail, RoomAvailabilityRetrieveView, RoomBookingAPIView

urlpatterns = [
    path('rooms/', RoomListView.as_view()),
    path('rooms/<int:pk>/', room_detail),
    path('rooms/<int:pk>/availability/', RoomAvailabilityRetrieveView.as_view()),
    path('rooms/<int:pk>/book/', RoomBookingAPIView.as_view()),
]

