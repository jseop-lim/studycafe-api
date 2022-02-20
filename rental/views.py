from rental.models import *
from rental.serializers import *

from rest_framework import generics
from rest_framework.response import Response


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
    

class StudentPurchaseView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = PurchaseStudentSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_object().purchases

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    
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


class PurchaseListView(generics.ListCreateAPIView):
    """
    List all purchases, or create a new purchase.
    """
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    
    # POST 요청 시에 호출되며, serializer data가 아닌 내부 처리로 필드값 할당
    def perform_create(self, serializer):
        serializer.save(student=self.request.user.student)
