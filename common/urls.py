from django.urls import path
from common import views

app_name = 'common'


urlpatterns = [
    path('', views.api_root),
    
    path('users', views.UserListView.as_view(), name='user-list'),
    path('users/<int:pk>', views.UserDetailView.as_view(), name='user-detail'),
]
