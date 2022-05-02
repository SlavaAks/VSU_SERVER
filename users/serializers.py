from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField()
    groups = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta(object):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'date_joined', 'password','groups')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        validated_data['groups'] = [2,]
        return super(UserSerializer, self).create(validated_data)