from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    residual_time = models.IntegerField(default=0)


class Ticket(models.Model):
    time = models.IntegerField()
    storable = models.BooleanField()
    price = models.IntegerField()
    student = models.ManyToManyField(Student, through='Purchase')
    

class Purchase(models.Model):
    student = models.ForeignKey(Student, primary_key=True, related_name='purchase', on_delete=models.SET_NULL)
    ticket = models.ForeignKey(Ticket, primary_key=True, related_name='purchase', on_delete=models.SET_NULL)
    date = models.DateTimeField(primary_key=True, auto_now_add=True)
    

class Seat(models.Model):
    student = models.ManyToManyField(Student, through='Rent')
    

class Rent(models.Model):
    student = models.ForeignKey(Student, primary_key=True, related_name='rent', on_delete=models.SET_NULL)
    seat = models.ForeignKey(Seat, primary_key=True, related_name='rent', on_delete=models.SET_NULL)
    start_date = models.DateTimeField(primary_key=True, auto_now_add=True)
    real_end_date = models.DateTimeField(blank=True)
    expected_end_date = models.DateTimeField()  # blank=True?