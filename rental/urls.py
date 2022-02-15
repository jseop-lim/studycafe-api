from django.urls import path
from rental import views

app_name = 'rental'


urlpatterns = [
    path('students', views.StudentListView.as_view(), name='student-list'),
    path('students/<int:pk>', views.StudentDetailView.as_view(), name='student-detail'),
]
