from rest_framework import serializers
from .models import Promo, PromoImage,User
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
     """just plainly returns the new instance"""
     class Meta:
          model = User
          fields = ('id','username','email')
     # returns the user data to the requesting user

class UserRegisterSerializer(serializers.ModelSerializer):
     """serializer is used to serialize and create new users in the system"""
     # serializes input for registering new users.
     class Meta:
          model = User
          fields = ('username','email','password')
          extra_kwargs = {'password':{'write_only': True}}

     def create(self,validated_data):
          user = User.objects.create_superuser(validated_data['username'],   # type: ignore
                                                  email=validated_data['email'],
                                                   password=validated_data['password'])
          return user


class UserLoginSerializer(serializers.Serializer):
     """for autthenticating and logging in users"""

     username = serializers.CharField()
     password = serializers.CharField()

     def validate(self, data):
          user = authenticate(**data)
          if user and user.is_active:
               return user

class PromoImageSerializer(serializers.ModelSerializer):
     class Meta:
          model = PromoImage
          fields = ("id","image","thumbnail")

class PromoSerializer(serializers.ModelSerializer):
     """serializes all promo objects"""
     image = serializers.StringRelatedField()
     class Meta:
          model = Promo
          fields = ("id","name","details","date","link","image")

          

          
     




class AddPromoSerializer(serializers.ModelSerializer):
     """"for adding new promo objects in the system"""
     class Meta:
          model = Promo
          fields = ('name','details','link')

