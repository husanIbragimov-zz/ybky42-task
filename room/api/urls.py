from django.urls import path
from .views import RoomListView, room_detail, RoomAvailabilityRetrieveView, RoomBookingAPIView, availability

urlpatterns = [
    path('rooms/', RoomListView.as_view()),
    path('rooms/<int:pk>/', room_detail),
    path('rooms/<int:pk>/abailability/', RoomAvailabilityRetrieveView.as_view()),
    path('rooms/<int:pk>/abailability2/', availability),
    path('rooms/<int:pk>/book/', RoomBookingAPIView.as_view()),
]

