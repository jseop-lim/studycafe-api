from rest_framework import serializers
from rental.models import Student, Ticket, Seat, Purchase, Rent
  
        
class TicketSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Ticket
        fields = ['id', 'time', 'storable', 'price']


class SeatSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Seat
        fields = ['id']

    
class PurchaseSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(read_only=True)
    ticket = serializers.PrimaryKeyRelatedField(queryset=Ticket.objects.all())
    
    class Meta:
        model = Purchase
        fields = ['id', 'student', 'ticket', 'date']
        
        
class PurchaseStudentSerializer(serializers.ModelSerializer):
    """
    student 필드를 제외한, read 용도의 purchase serializer
    """
    ticket = serializers.StringRelatedField()
    
    class Meta:
        model = Purchase
        fields = ['id', 'ticket', 'date']
        

class RentSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(read_only=True)
    seat = serializers.PrimaryKeyRelatedField(queryset=Seat.objects.all())
    
    class Meta:
        model = Rent
        fields = ['id', 'student', 'seat', 'start_date', 'expected_end_date']
        read_only_fields = ['start_date', 'expected_end_date']


class RentStudentSerializer(serializers.ModelSerializer):
    """
    student 필드를 제외한, read 용도의 rent serializer
    """
    seat = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Rent
        fields = ['id', 'seat', 'start_date', 'real_end_date']


class StudentSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='user.id')
    purchases = PurchaseStudentSerializer(many=True, read_only=True)
    rents = RentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Student
        fields = ['id', 'name', 'residual_time', 'storable', 'purchases', 'rents']
        read_only_fields = ['residual_time', 'storable']