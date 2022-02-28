from rental.models import Seat, Rent
from rental.serializers import SeatSerializer, RentSerializer

from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.exceptions import ValidationError

from celery import shared_task


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
        student = self.request.user.student
        exp_end_date = timezone.now() + timezone.timedelta(seconds=student.residual_time)
        rent = serializer.save(student=student, expected_end_date=exp_end_date)
        update_real_end_date.apply_async(args=[rent.pk], eta=rent.expected_end_date)
    
    def create(self, request, *args, **kwargs):
        """
        Create a rent instance when the student's residual time is greater than 0.
        """
        if self.request.user.student.residual_time == 0:
            raise ValidationError({"student": ["There is no residual time, so please purchase a ticket."]})
        else:
            return super().create(request, *args, **kwargs)
        

class RentDetailView(generics.RetrieveUpdateAPIView):
    """
    Retrieve a rent.
    """
    queryset = Rent.objects.all()
    serializer_class = RentSerializer
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.real_end_date = timezone.now()
            
        if instance.student.storable:
            instance.student.residual_time = \
                (instance.expected_end_date - instance.real_end_date).total_seconds()
        else:
            instance.student.residual_time = 0
            
        instance.student.save()
        instance.save()
        return Response("The rental has ended.")


@shared_task
def update_real_end_date(pk):
    rent = Rent.objects.get(pk=pk)
    if not rent.real_end_date:
        rent.real_end_date = rent.expected_end_date        
        rent.student.residual_time = 0
        rent.student.storable = False
        rent.student.save()
        rent.save()