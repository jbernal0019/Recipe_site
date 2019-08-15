
from django.contrib.auth.models import User

from rest_framework import generics, permissions

from collectionjson import services

from .serializers import UserSerializer
from .permissions import IsUser


class UserCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        """
        Overriden to append a collection+json write template.
        """
        response = services.get_list_response(self, [])
        template_data = {"username": "",  "email": "", "password": "", "first_name": "",
                         "last_name": ""}
        return services.append_collection_template(response, template_data)


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsUser)
