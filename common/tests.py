import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from django.contrib.auth.models import User
from common.serializers import UserSerializer
from rental.models import Student

    
class UserViewTest(APITestCase):
    # def setUp(self):
    #     self.factory = APIRequestFactory()
    
    
    def create_user(self, login=False):
        user = User.objects.create_user(username='user', password='1234', email="user@example.com")
        student = Student.objects.create(user=user, name='Kim')
        if login:
            self.client.force_authenticate(user)
        
        return user
    
    
    def test_user_create_shell(self):
        """
        Django ORM을 이용한 User 생성
        """
        user = self.create_user()
        
        self.assertEqual(user.student.user_id, user.id)
        self.assertEqual(user.student.name, 'Kim')
        self.assertEqual(user.student.residual_time, 0)
    
    
    def test_user_create_api(self):
        """
        UserListView를 이용한 User 생성
        """
        data = {"username": "user1", "password": "qlalfqjsgh1234", "email": "user1@example.com", "student": {"name": "Park"}}
        response = self.client.post(reverse('common:user-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username='user1')
        
        # 로그인
        self.assertTrue(self.client.login(username='user1', password='qlalfqjsgh1234'))
        
        response = self.client.get(reverse('common:user-detail', args=[user.id]), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, user)
    
    
    def test_user_detail(self):
        """
        Django ORM으로 생성한 User를 user-detail api에서 읽기
        """
        user = self.create_user(login=True)
        
        response = self.client.get(reverse('common:user-detail', args=[user.id]), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, user)


    def test_user_list(self):
        """
        user-list api에서 json response와 모든 user instance 비교
        """
        user1 = self.create_user()
        user2 = User.objects.create_user(username='user2', password='5678')
        student = Student.objects.create(user=user2, name='Lee')
        
        response = self.client.get(reverse('common:user-list'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        serializer = UserSerializer(User.objects.all(), many=True)
        self.assertEqual(User.objects.count(), 2)
        self.assertJSONEqual(response.content, serializer.data)
    
    
    def test_user_update(self):
        """
        user-update api에서 email과 student name 변경
        """
        user = self.create_user(login=True)
        
        # email, student name 동시에 변경
        data = {"email": "changed_one@example.com", "student": {"name": "One"}}
        response = self.client.put(reverse('common:user-detail', args=[user.id]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get(pk=user.id)
        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.student.name, data['student']['name'])
        
        # email만 변경
        data = {"email": "changed_two@example.com"}
        # data = {"email": "changed_two@example.com", "student": {}}  # Fail
        response = self.client.put(reverse('common:user-detail', args=[user.id]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get(pk=user.id)
        self.assertEqual(user.email, data['email'])
        
        # student name만 변경
        data = {"student": {"name": "Three"}}
        response = self.client.put(reverse('common:user-detail', args=[user.id]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get(pk=user.id)
        self.assertEqual(user.student.name, data['student']['name'])
        
    
    def test_user_password_change_validation(self):
        """
        user-password api에서 password change 유효성 검사 테스트
        """
        user = self.create_user(login=True)
        
        # old_password field error
        data = {"old_password": "incorrect", "password": "newpw1234", "password2": "newpw1234"}
        response = self.client.put(reverse('common:user-password', args=[user.id]), data, format='json')
        self.assertContains(response, "Old password is not correct.", status_code=status.HTTP_400_BAD_REQUEST)
        
        # password field error
        data = {"old_password": "1234", "password": "1234", "password2": "1234"}
        response = self.client.put(reverse('common:user-password', args=[user.id]), data, format='json')
        self.assertContains(response, "비밀번호가 너무 짧습니다. 최소 8 문자를 포함해야 합니다.", status_code=status.HTTP_400_BAD_REQUEST)
        
        # password non-field error
        data = {"old_password": "1234", "password": "newpw1234", "password2": "different"}
        response = self.client.put(reverse('common:user-password', args=[user.id]), data, format='json')
        self.assertContains(response, "Password fields didn't match.", status_code=status.HTTP_400_BAD_REQUEST)
    
    
    def test_user_password_change_api(self):
        """
        user-password api에서 password change 작동 테스트
        """
        user = self.create_user(login=True)
        
        # 비밀번호 변경
        data = {"old_password": "1234", "password": "newpw1234", "password2": "newpw1234"}
        response = self.client.put(reverse('common:user-password', args=[user.id]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 로그아웃
        self.client.logout()
        
        # 기존 비밀번호로 로그인 시도
        self.assertFalse(self.client.login(username='user', password='1234'))
        
        # 새로운 비밀번호로 로그인 성공
        self.assertTrue(self.client.login(username='user', password='newpw1234'))