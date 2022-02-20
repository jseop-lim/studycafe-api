from django.contrib.auth.models import User
from common.serializers import UserCreateReadSerializer, UserUpdateSerializer
from common.serializers import PasswordChangeSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import mixins, generics

from rest_framework import permissions
from common.permissions import IsOwner, AdminReadOnly


@api_view(['GET'])
def api_root(request, format=None):
    """
    Root view
    """
    return Response({
        'users': reverse('common:user-list', request=request, format=format),
        'students': reverse('rental:student-list', request=request, format=format),
        'tickets': reverse('rental:ticket-list', request=request, format=format),
        'purchases': reverse('rental:purchase-list', request=request, format=format),
        'seats': reverse('rental:seat-list', request=request, format=format),
    })


class UserListView(generics.GenericAPIView,
                   mixins.ListModelMixin, mixins.CreateModelMixin):
    """
    List all users, or create a new user.
    """
    queryset = User.objects.all()
    serializer_class = UserCreateReadSerializer
    permission_classes = [
        permissions.AllowAny,
    ]
    
    # TODO user-detail api의 hyperlink list로 수정
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UserDetailView(generics.RetrieveUpdateAPIView):
    """
    Retrieve, update a user.
    """
    queryset = User.objects.all()
    serializer_class = UserCreateReadSerializer
    permission_classes = [
        AdminReadOnly | IsOwner
    ]
    
    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return UserUpdateSerializer
        return self.serializer_class
    
    # def delete(self, request, *args, **kwargs):
    #     return self.destroy(request, *args, **kwargs)
    
    
class PasswordChangeView(generics.UpdateAPIView):
    """
    Update password of a user.
    """
    queryset = User.objects.all()
    serializer_class = PasswordChangeSerializer
    permission_classes = [
        IsOwner,
    ]
        