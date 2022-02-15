from rest_framework import serializers
from rental.models import Student, Ticket, Seat, Purchase, Rent
  
        
# class TicketSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = Ticket
#         fields = ['id', 'time', 'storable', 'price']


# class SeatSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = Seat
#         fields = ['id']

    
# class PurchaseSerializer(serializers.ModelSerializer):
#     student = serializers.PrimaryKeyRelatedField(write_only=True)
#     ticket = serializers.PrimaryKeyRelatedField()
    
#     class Meta:
#         model = Purchase
#         fields = ['id', 'student', 'ticket', 'date']
        

# class RentSerializer(serializers.ModelSerializer):
#     student = serializers.PrimaryKeyRelatedField(write_only=True)
#     seat = serializers.PrimaryKeyRelatedField()
    
#     class Meta:
#         model = Rent
#         fields = ['id', 'student', 'seat',
#                   'start_date', 'real_end_date', 'expected_end_date']


class StudentSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='user.id')
    # purchases = PurchaseSerializer(source='purchases', many=True, read_only=True)
    # rents = RentSerializer(source='rents', many=True, read_only=True)
    
    class Meta:
        model = Student
        fields = ['id', 'name', 'residual_time', 'purchases', 'rents']
