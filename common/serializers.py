from rest_framework import serializers
from django.contrib.auth.models import User
from rental.models import Student
from rental.serializers import StudentSerializer

class UserSerializer(serializers.ModelSerializer):
    student = StudentSerializer(required=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'student']
        extra_kwargs = {'password': {'write_only': True}}
        
        
    def create(self, validated_data):
        # create user
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
        )
        
        # create student
        student_data = validated_data.pop('student')
        student = Student.objects.create(
            user = user,
            name = student_data['name'],
        )

        return user