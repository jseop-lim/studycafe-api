import json
from django.urls import reverse
from rest_framework import status
from django.test import tag
from rest_framework.test import APITestCase, APISimpleTestCase
from rental.models import *
from rental.serializers import PurchaseStudentSerializer
from django.utils import timezone
import time

from celery.contrib.testing.worker import start_worker
from config.celery import app

    
class PurchaseViewTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.tickets = {}
        cls.tickets[1] = Ticket.objects.create(time=10, storable=False, price=1000)
        cls.tickets[2] = Ticket.objects.create(time=5, storable=True, price=1500)
    
    
    def create_user(self, login=False, username='user', password='1234', email="user@test.com", name='Kim'):
        user = User.objects.create_user(username, email, password)
        student = Student.objects.create(user=user, name=name)
        if login:
            self.assertTrue(self.client.login(username=username, password=password))
        return user

    
    def test_purchase_create_api(self):
        """
        purchase-list에서 POST 요청으로 purchase 생성
        """
        student = self.create_user(login=True).student
        residual_time = student.residual_time
        ticket = self.tickets[2]  # 0:00:05 / 1,500원 (storable)
        
        data = {"ticket": ticket.id}
        response = self.client.post(reverse('rental:purchase-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # purchase 필드 일치 확인
        purchase = Purchase.objects.get(pk=json.loads(response.content)['id'])
        self.assertEqual(purchase.student, student)
        self.assertEqual(purchase.ticket, ticket)
        
        # student 필드 변경 확인
        student.refresh_from_db()
        self.assertEqual(student.residual_time, residual_time + ticket.time)
        self.assertTrue(student.storable == ticket.storable == True)  # False -> True로 바뀜
        
    
    @tag('shell')
    def test_purchase_create_shell(self):
        """
        Django ORM을 이용한 purchase 생성
        (model receiver 적용 시 student 필드 값 변경)
        """
        student = self.create_user(login=True).student
        residual_time = student.residual_time
        ticket = self.tickets[2]  # 0:00:05 / 1,500원 (storable)
        
        # purchase 필드 일치 확인
        purchase = Purchase.objects.create(student=student, ticket=ticket)
        self.assertEqual(purchase.student, student)
        self.assertEqual(purchase.ticket, ticket)
        
        # student 필드 변경 확인
        student.refresh_from_db()
        self.assertEqual(student.residual_time, residual_time + ticket.time)
        self.assertEqual(student.storable, ticket.storable)  # False -> True로 바뀌지 않음
    

class StudentViewTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.tickets = {}
        cls.tickets[1] = Ticket.objects.create(time=10, storable=False, price=1000)
        cls.tickets[2] = Ticket.objects.create(time=5, storable=True, price=1500)
    
    
    def create_user(self, login=False, username='user', password='1234', email="user@test.com", name='Kim'):
        user = User.objects.create_user(username, email, password)
        student = Student.objects.create(user=user, name=name)
        if login:
            self.assertTrue(self.client.login(username=username, password=password))
        return user
    

    def test_student_purchase(self):
        """
        student-purchase에서 학생과 연결된 purchases가 잘 나오는지 확인
        """
        std1 = self.create_user(username='user1', name='Kim').student
        Purchase.objects.create(student=std1, ticket=self.tickets[1])
        Purchase.objects.create(student=std1, ticket=self.tickets[1])
        Purchase.objects.create(student=std1, ticket=self.tickets[2])
        
        std2 = self.create_user(username='user2', name='Lee').student
        Purchase.objects.create(student=std2, ticket=self.tickets[1])
        
        std1.refresh_from_db()
        serializer = PurchaseStudentSerializer(std1.purchases, many=True)
        
        response = self.client.get(reverse('rental:student-purchase', args=[std1.user_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, serializer.data)


class RentViewTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.seat = Seat.objects.create()
        # cls.celery_worker = start_worker(app, perform_ping_check=False)
        # cls.celery_worker.__enter__()
    
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        # cls.celery_worker.__exit__(None, None, None)
        app.control.purge()

    
    def create_user(self, login=False, username='user', password='1234', email="user@test.com", name='Kim'):
        user = User.objects.create_user(username, email, password)
        student = Student.objects.create(user=user, name=name)
        if login:
            self.assertTrue(self.client.login(username=username, password=password))
        return user

    
    def test_rent_create_api(self):
        """
        rent-list에서 POST 요청으로 rent 생성
        """
        student = self.create_user(login=True).student
        student.residual_time = 61
        student.save()
        
        data = {"seat": self.seat.id}
        response = self.client.post(reverse('rental:rent-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # rent 필드 일치 확인
        rent = Rent.objects.get(pk=json.loads(response.content)['id'])
        self.assertEqual(rent.student, student)
        self.assertEqual(rent.seat, self.seat)
        date_diff = (rent.expected_end_date - rent.start_date).total_seconds()
        self.assertEqual(round(date_diff, 2), student.residual_time)
        
    
    @tag('shell')
    def test_rent_create_shell(self):
        """
        Django ORM을 이용한 rent 생성
        (pre_save signal로 expected_end_date 필드 값 초기화)
        """
        student = self.create_user().student
        student.residual_time = 61
        student.save()
        rent = Rent.objects.create(student=student, seat=self.seat)
        
        # rent 필드 일치 확인
        self.assertEqual(rent.student, student)
        self.assertEqual(rent.seat, self.seat)
        date_diff = (rent.expected_end_date - rent.start_date).total_seconds()
        self.assertEqual(round(date_diff, 2), student.residual_time)
    
    
    def test_rent_end_manual_non_store(self):
        """
        예정마감일시 이전에 학생이 수동으로 대여를 마감하는 경우 (저장 X)
        """
        # 학생 객체 생성 및 필드 초기화
        student = self.create_user(login=True).student
        student.residual_time = 10
        student.storable = False
        student.save()
        
        # 대여 시작
        data = {"seat": self.seat.id}
        response = self.client.post(reverse('rental:rent-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        time.sleep(2)
        rent = Rent.objects.get(pk=json.loads(response.content)['id'])
        
        # 대여 마감
        response = self.client.put(reverse('rental:rent-detail', args=[rent.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
        student.refresh_from_db()
        rent.refresh_from_db()
        time_diff = (rent.expected_end_date - rent.real_end_date).total_seconds()
        self.assertEqual(round(time_diff, 1), 8)
        self.assertEqual(student.residual_time, 0)
        self.assertEqual(student.storable, False)


    def test_rent_end_manual_store(self):
        """
        예정마감일시 이전에 학생이 수동으로 대여를 마감하는 경우 (저장 O)
        """
        # 학생 객체 생성 및 필드 초기화
        student = self.create_user(login=True).student
        student.residual_time = 10
        student.storable = True
        student.save()
        
        # 대여 시작
        data = {"seat": self.seat.id}
        response = self.client.post(reverse('rental:rent-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        time.sleep(2)
        rent = Rent.objects.get(pk=json.loads(response.content)['id'])
        
        # 대여 마감
        response = self.client.put(reverse('rental:rent-detail', args=[rent.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
        student.refresh_from_db()
        rent.refresh_from_db()
        time_diff = (rent.expected_end_date - rent.real_end_date).total_seconds()
        self.assertEqual(round(time_diff, 1), 8)
        self.assertEqual(student.residual_time, int(time_diff))
        self.assertEqual(student.storable, True)
    


class CeleryTest(APISimpleTestCase):
    databases = '__all__'
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.celery_worker = start_worker(app, perform_ping_check=False)
        cls.celery_worker.__enter__()
    
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.celery_worker.__exit__(None, None, None)


    def test_rent_end_auto(self):
        """
        예정마감일시가 되면 자동으로 대여를 마감
        """
        # 학생 객체 생성 및 필드 초기화
        user = User.objects.create_user(username='user', password='1234', email="user@test.com")
        student = Student.objects.create(user=user, name='Kim', residual_time=2, storable=True)
        self.assertTrue(self.client.login(username='user', password='1234'))
        seat = Seat.objects.create()
        
        # 대여 시작
        data = {"seat": seat.id}
        response = self.client.post(reverse('rental:rent-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        time.sleep(3)
        
        # 자동 대여 마감
        student.refresh_from_db()
        rent = Rent.objects.get(pk=json.loads(response.content)['id'])
        self.assertEqual(rent.expected_end_date, rent.real_end_date)
        self.assertEqual(student.residual_time, 0)
        self.assertEqual(student.storable, False)