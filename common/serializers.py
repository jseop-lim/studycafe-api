from rest_framework import serializers
from django.contrib.auth.models import User
from rental.models import Student
from rental.serializers import StudentSerializer

from django.contrib.auth.password_validation import validate_password


class UserCreateReadSerializer(serializers.ModelSerializer):
    """
    Serializer for user create, retrieve
    """
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)
    student = StudentSerializer(required=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'password2', 'email', 'student']
    
    def create(self, validated_data):
        # create user
        user = User.objects.create_user(
            username = validated_data['username'],
            password = validated_data['password'],
            email = validated_data['email'],
        )
        
        # create student
        student_data = validated_data.pop('student')
        student = Student.objects.create(
            user = user,
            name = student_data['name'],
        )
        # TODO refactor: https://stackoverflow.com/questions/37240621/django-rest-framework-updating-nested-object
        return user

    def validate(self, attrs):
        """
        password, password2 일치 여부 검사
        """    
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password2": "Password fields didn't match."})
        return super().validate(attrs)


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for user update.
    """
    student = StudentSerializer(required=False)  # TODO: partial-update
    
    class Meta:
        model = User
        fields = ['email', 'student']
            
    def update(self, instance, validated_data):
        """
        Explicit update() method for nested serializer field.
        """
        student = validated_data.pop('student', {})
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        # instance.email = validated_data.get('email', instance.email)
        instance.save()
                    
        for attr, value in student.items():
            setattr(instance.student, attr, value)
        instance.student.save()
        
        return instance


class PasswordChangeSerializer(serializers.ModelSerializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['old_password', 'password', 'password2']

    def update(self, instance, validated_data):
        """
        Explicit update() method for set password.
        """
        instance.set_password(validated_data['password'])
        instance.save()
        return instance
    
    def validate_old_password(self, value):
        """
        old_password 일치 여부 검사
        """
        if not self.instance.check_password(value):
            raise serializers.ValidationError("Old password is not correct.")
        return value
    
    def validate(self, attrs):
        """
        password, password2 일치 여부 검사
        """    
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password2": "Password fields didn't match."})
        return super().validate(attrs)