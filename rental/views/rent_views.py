from rental.models import Seat
from rental.serializers import SeatSerializer

from rest_framework import generics


class SeatListView(generics.ListCreateAPIView):
    """
    List all seats, or create a new seat.
    """
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    
    
class SeatDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a seat.
    """
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer