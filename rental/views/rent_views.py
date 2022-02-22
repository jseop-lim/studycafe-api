from django.utils import timezone

from rental.models import Seat, Rent
from rental.serializers import SeatSerializer, RentSerializer

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
    
    
class RentListView(generics.ListCreateAPIView):
    """
    List all rents, or create a new rent.
    """
    queryset = Rent.objects.all()
    serializer_class = RentSerializer
    
    # POST 요청 시에 호출되며, serializer data가 아닌 내부 처리로 필드값 할당
    def perform_create(self, serializer):
        serializer.save(student=self.request.user.student)
        

class RentDetailView(generics.RetrieveAPIView):
    """
    Retrieve a rent.
    """
    queryset = Rent.objects.all()
    serializer_class = RentSerializer
    