from django.urls import path
from .views import RoomListView, room_detail, availability, book_create

urlpatterns = [
    path('rooms/', RoomListView.as_view()),
    path('rooms/<int:pk>/', room_detail),
    path('rooms/<int:pk>/abailability/', availability),
    path('rooms/<int:pk>/book/', book_create),
]
