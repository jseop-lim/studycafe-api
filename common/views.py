from django.contrib.auth.models import User
from common.serializers import UserSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import mixins, generics

# TODO permission


@api_view(['GET'])
def api_root(request, format=None):
    """
    Root view
    """
    return Response({
        'users': reverse('common:user-list', request=request, format=format),
        'students': reverse('rental:student-list', request=request, format=format)
    })


class UserListView(generics.GenericAPIView,
                   mixins.ListModelMixin, mixins.CreateModelMixin):
    """
    List all users, or create a new user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UserDetailView(generics.GenericAPIView,
                     mixins.RetrieveModelMixin):
    """
    Retrieve, update or delete a user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    # def put(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)

    # def delete(self, request, *args, **kwargs):
    #     return self.destroy(request, *args, **kwargs)