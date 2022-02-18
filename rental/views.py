from rental.models import Student
from rental.serializers import StudentSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status


class StudentListView(APIView):
    """
    List all students.
    """
    def get(self, request, format=None):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)


class StudentDetailView(APIView):
    """
    Retrieve a student.
    """
    def get_object(self, pk):
        return get_object_or_404(Student, pk=pk)
        
    def get(self, request, pk, format=None):
        student = self.get_object(pk)
        serializer = StudentSerializer(student)
        return Response(serializer.data)
