from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import CustomUserSerializer,login_User_serilazier,ProviderSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser ,provider, Recipient

class register (GenericAPIView): 
    serilaizer = CustomUserSerializer

    def post (self , request):
        serilaizer = CustomUserSerializer(data=request.data)
        if serilaizer.is_valid():
            serilaizer.save()
            return Response(
                serilaizer.data, status = status.HTTP_201_CREATED
            )
        return Response(
            serilaizer.errors,status=status.HTTP_400_BAD_REQUEST
        )
# Create your views here.
"""
class login (GenericAPIView):
    def post (self, request):
        data=request.data
        serializer = logiserilazier(data)
        email = data.get('email')
        password = data.get('password')

        user = serializer.login(email,password)
        user_instance = CustomUser.objects.get(email=email)

        #if user_instance.usertype == 'provider':



        serilaizer2 = CustomUserSerializer(user_instance)
        if  user : 
            return Response(
                serilaizer2.data, status = status.HTTP_200_OK
            )
        else :return Response(
            serializer.errors,status=status.HTTP_404_NOT_FOUND\
            
        )

"""


class loginview (GenericAPIView):
    def post (self, request):
        data=request.data
        serializer = login_User_serilazier(data)
        username = data.get('username')
        password = data.get('password')
        user = serializer.login(username,password)
        
        user_instance = CustomUser.objects.get(username=username)
        
        if user_instance.usertype == 'provider':
            user_instance = provider.objects.get(username=username)
            serializer = ProviderSerializer(user_instance)
        elif user_instance.usertype == 'recipient' :
            user_instance = CustomUser.objects.get(username=username)
            serializer = CustomUserSerializer(user_instance)
        else : raise NameError
        
        if  user : 
            return Response(
                serializer.data, status = status.HTTP_200_OK
            )
        else :return Response(
            serializer.errors,status=status.HTTP_404_NOT_FOUND
        )