from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.db import IntegrityError
from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField()
    groups = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta(object):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'date_joined', 'password','city','country','phone','avatar','groups')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):

        validated_data['password'] = make_password(validated_data['password'])
        try:
            validated_data['groups'] = [2]
            Group.objects.get(name='student')
        except IntegrityError:
            if len(Group.objects.all())==0:
                Group.objects.create(name='teacher')
                Group.objects.create(name='student')
            else:
                Group.objects.create(name='student')
        finally:
            return super(UserSerializer, self).create(validated_data)

        return super(UserSerializer, self).create(validated_data)

    def update(self,request,user_data):
        user=request.user
        user.email=user_data["email"]
        user.first_name=user_data["first_name"]
        user.last_name=user_data["last_name"]
        user.city=user_data["city"]
        user.country=user_data["country"]
        user.phone=int(user_data["phone"])
        print(user_data["avatar"].__dict__,"ss")
        user.avatar=user_data["avatar"]
        user.save()
        return user