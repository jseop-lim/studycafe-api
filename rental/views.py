from rental.models import Student, Ticket
from rental.serializers import StudentSerializer, TicketSerializer

from rest_framework import generics


class StudentListView(generics.ListAPIView):
    """
    List all students.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentDetailView(generics.RetrieveAPIView):
    """
    Retrieve a student.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    
class TicketListView(generics.ListCreateAPIView):
    """
    List all tickets, or create a new ticket.
    """
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    
    
class TicketDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a ticket.
    """
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

