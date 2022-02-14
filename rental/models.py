from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    residual_time = models.IntegerField(default=0)
    tickets = models.ManyToManyField('Ticket', through='Purchase', related_name='students')
    seats = models.ManyToManyField('Seat', through='Rent', related_name='students')


class Ticket(models.Model):
    time = models.IntegerField()
    storable = models.BooleanField()
    price = models.IntegerField()
    

class Purchase(models.Model):
    student = models.ForeignKey(Student, related_name='purchases', on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, related_name='purchases', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    

class Seat(models.Model):
    pass
    

class Rent(models.Model):
    student = models.ForeignKey(Student, related_name='rents', on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, related_name='rents', on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    real_end_date = models.DateTimeField(blank=True)
    expected_end_date = models.DateTimeField()  # blank=True?