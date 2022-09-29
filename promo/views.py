from ast import Delete
from urllib import request
from .serializers import (PromoSerializer,AddPromoSerializer,PromoImageSerializer,
UserRegisterSerializer,UserLoginSerializer, UserSerializer)
from rest_framework.views import APIView
from django.db.models.query import QuerySet
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes,parser_classes
from rest_framework import permissions,generics
from rest_framework.parsers import FileUploadParser
from knox.models import AuthToken
from .models import Promo,PromoImage
from django.core.files.uploadedfile import InMemoryUploadedFile

class UserView(generics.GenericAPIView):
     serializer_class = UserSerializer
     permission_classes = [permissions.IsAuthenticated]


     def get(self,request,*args,**kwargs):
          if request.user: #if user asspciated with the token, return the user
               return Response(data=UserSerializer(request.user).data,status=status.HTTP_200_OK)
          return Response({"erro":"User not found"},status.HTTP_404_NOT_FOUND)


class RegisterUser(generics.GenericAPIView):
     """view for handling user registration"""
     # serializer for serializing input
     serializer_class = UserRegisterSerializer
     def post(self,request: Request,*args,**kwargs):
          try:
               serialized = self.get_serializer(data=request.data)
               serialized.is_valid(raise_exception=True)
               user = serialized.save()
               token = AuthToken.objects.create(user)
               return Response(
                    {'user': UserSerializer(user,context=self.get_serializer_context()).data,
                    'token': token[1]
                    },status=status.HTTP_201_CREATED
               )
          except Exception as err:
               return Response({"details":"Input not valid"})
          
class LoginUser(APIView):
     """view for handling user login"""
     def post(self,request):
          ser = UserLoginSerializer(data=request.data)
          # we have to call is_valid() before validated data can accessed.
          try:
               ser.is_valid(raise_exception=True)
               user = ser.validated_data
               if user:
                    # create token for the new logged in user
                    token = AuthToken.objects.create(user)
                    return Response({'user': UserSerializer(user).data,
                    'token': token[1]},status=status.HTTP_200_OK)
          except Exception as err:
               return Response("User is not valid",status=status.HTTP_400_BAD_REQUEST)

#+++++++=+++++++++++++++++++++++++++++++++++++++


@api_view(["GET"])
def get_all(request: Request):
     data = Promo.objects.prefetch_related('image')
     list_data = PromoSerializer(data,many=True).data
     # returns all the list of promos
     return Response(list_data,status=status.HTTP_200_OK)

@api_view(["GET"])
def get_detail_promo(request: Request,id):
     obj = PromoView.get_object(id=id)
     if obj:
          data = PromoSerializer(obj).data
          return Response(data,status=status.HTTP_200_OK)
     
     return Response({"details":"Promo not found"},status=status.HTTP_404_NOT_FOUND)
# Create your views here.

class PromoView(APIView):
     permission_classes = [permissions.IsAuthenticated,]

     @staticmethod
     def get_object(id):
          # try to get object from db except object does not exist
          try:
               if id > 0:
                    # check if an is provided
                    data = Promo.objects.get(id=id)
                    return data
          except Promo.DoesNotExist:
               return None
               
    
     def get(self,request: Request,id,*args,**kwargs):
          """Retrieves an instance of a promo"""
          # get object 
          if id > 0: 
               obj = PromoView.get_object(id)
               data = PromoSerializer(obj)
               
               return Response(data.data)     
          elif id == 0:
               data = Promo.objects.prefetch_related('image')
               return Response(PromoSerializer(data, many= True).data)
          return Response({"details":"Object not found"},status=status.HTTP_404_NOT_FOUND,exception=True)

     def post(self,request,*args,**kwargs):
          try:
               serializer = PromoSerializer(data=request.data)
               serializer.is_valid(raise_exception=True)
               promo = serializer.save(admin=request.user)
               return Response(data=PromoSerializer(promo).data,status=status.HTTP_201_CREATED)
          except Exception as e:
               print(e)
               return Response({"details":"Something went wrong on the server"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,exception=True)
          

     def delete(self,request: Request,id,*args,**kwargs):
          if id==0:
               return Response({"details":"Invalid id"},status=status.HTTP_400_BAD_REQUEST)
          data = PromoView.get_object(id)  
          if data:
               data.delete()
               return Response(status=status.HTTP_204_NO_CONTENT)
          return Response({"details":"Could not delete!"},status=status.HTTP_400_BAD_REQUEST,exception=True)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
@parser_classes([FileUploadParser])
def post_image(request: Request, id):
     data: InMemoryUploadedFile = request.data['file']  # type: ignore
     try:
          p = Promo.objects.get(id=id)
          if p:
               image = PromoImage(promo=p,image=data)
               image.save()
               image.refresh_from_db()
               return Response(PromoImageSerializer(image).data)
     except Promo.DoesNotExist as e:
          print(e)
          return Response({"details":"Advert or post does not Exist"},
                    status=status.HTTP_400_BAD_REQUEST)

          

