from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from celery import shared_task


class Student(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    residual_time = models.IntegerField(default=0)
    storable = models.BooleanField(default=False)
    tickets = models.ManyToManyField('Ticket', through='Purchase', related_name='students')
    seats = models.ManyToManyField('Seat', through='Rent', related_name='students')
    
    class Meta:
        ordering = ['user_id']


class Ticket(models.Model):
    time = models.IntegerField()
    storable = models.BooleanField()
    price = models.IntegerField()
    
    class Meta:
        ordering = ['storable', 'time']
    
    def __str__(self):
        ret = f'{timezone.timedelta(seconds=self.time)} / {self.price:,}원'
        if self.storable:
            ret += ' (storable)'
        return ret
        

class Purchase(models.Model):
    student = models.ForeignKey(Student, related_name='purchases', on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, related_name='purchases', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']


# @receiver(post_save, sender=Purchase)
# def update_student_after_purchase(sender, instance, created, **kwargs):
#     if created:
#         instance.student.residual_time += instance.ticket.time
#         instance.student.storable = instance.ticket.storable
#         instance.student.save()


class Seat(models.Model):
    
    class Meta:
        ordering = ['id']
    

class Rent(models.Model):
    student = models.ForeignKey(Student, related_name='rents', on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, related_name='rents', on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    real_end_date = models.DateTimeField(null=True, blank=True)
    expected_end_date = models.DateTimeField()
    
    class Meta:
        ordering = ['-start_date']
    
    # def save(self, *args, **kwargs):
    #     created = self._state.adding
    #     if created:
    #         self.expected_end_date = timezone.now() + \
    #             timezone.timedelta(seconds=self.student.residual_time)

    #     super().save(*args, **kwargs)
        
    #     if created:
    #         update_real_end_date.apply_async(args=[self.pk], eta=self.expected_end_date)


# @shared_task
# def update_real_end_date(pk):
#     rent = Rent.objects.get(pk=pk)
#     if not rent.real_end_date:
#         rent.student.storable = False
#         rent.student.save()
#         rent.real_end_date = rent.expected_end_date
#         rent.save()


# @receiver(post_save, sender=Rent)
# def update_student_after_rent(sender, instance, created, **kwargs):
#     if not created:
#         residual_time = 0
#         if instance.student.storable:
#             residual_time = (instance.expected_end_date - instance.real_end_date).total_seconds()

#         instance.student.residual_time = residual_time
#         instance.student.save()
