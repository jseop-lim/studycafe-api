import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rental.models import *
from rental.serializers import PurchaseStudentSerializer

    
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
        
        