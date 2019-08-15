
from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.HyperlinkedModelSerializer):
    recipe = serializers.HyperlinkedRelatedField(view_name='recipe-detail',
                                                 read_only=True)
    username = serializers.CharField(max_length=50,
                                     validators=[UniqueValidator(
                                         queryset=User.objects.all())])
    email = serializers.EmailField(required=True,
                                   validators=[UniqueValidator(
                                       queryset=User.objects.all())])
    password = serializers.CharField(min_length=6, max_length=100, write_only=True)

    def create(self, validated_data):
        """
        Overriden to take care of the password hashing.
        """
        username = validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data.get('password')
        first_name = validated_data.get('first_name', '')
        last_name = validated_data.get('last_name', '')
        return User.objects.create_user(username, email, password, first_name=first_name,
                                        last_name=last_name)

    class Meta:
        model = User
        fields = ('url', 'username', 'first_name', 'last_name', 'email', 'password',
                  'recipe')
