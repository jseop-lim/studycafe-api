from rental.models import Student
from rental.serializers import StudentSerializer, PurchaseStudentSerializer

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
    """
    List all purchases of a student.
    """
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