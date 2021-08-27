from django.shortcuts import render
from rest_framework import response

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, logout
from .models import *
from .serializer import *


class SignUpAPI(APIView):
    def post(self, request):
        try:
            data =request.data
            serializers=CustomUserSerializer(data=data)
            if serializers.is_valid():
                name = serializers.data["name"]
                email = serializers.data["email"]
                password = serializers.data["password"]
                phone = serializers.data["phone"]

                if CustomUser.objects.filter(email=email).first():
                    return Response({"status":400, "result":"Acount already exists."})
                else:
                    tok = str(uuid.uuid4())
                    new_user = CustomUser.objects.create(email=email, name=name, phone=phone)
                    new_user.set_password(password)
                    new_user.save()
                    return Response({
                        "status":200, 
                        "result":"Accont created succesfully" ,
                         "data":serializers.data
                         })
            return Response({"status":400, "error":serializers.errors})

        except Exception as e:
            print(e)
        return Response({"status":500, "message":"something went wrong"})


class LoginAPI(APIView):
    def post(self ,request):
        try:
            data=request.data
            serializers=loginSerializer(data=data)
            if serializers.is_valid():
                email = serializers.data["email"]
                password = serializers.data["password"]
                user_obj = CustomUser.objects.filter(email=email).first()
                if user_obj is None:
                    return Response({"status":400, "result":"Account does not exist"})
                
                user = authenticate(email=email, password=password)
                
                refresh = RefreshToken.for_user(user)

                return Response({
                            "status":200,
                            "result":"Welcome User Login successfully",
                            'refresh': str(refresh),
                            'access': str(refresh.access_token)
                            })
            
            return Response({"status":400, "error":serializers.errors})
        except Exception as e:
            print(e)
        return Response({"status":500, "message":"something went wrong"})

class EventAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self ,request):
        try:
            print(request.user)
            user =Event.objects.filter(user=request.user)
            serializers=EventSerializer(user,many = True)
            return Response({
                            "status":200,
                            "result":"welcome following are your Event",
                            "data" : serializers.data 
            })

        except Exception as e:
            print(e)
        return Response({"status":500, "message":"something went wrong"})

    def post(self,request):
        try:
            request.data['user']=request.user.id
            serializers=EventSerializer(data=request.data)
            if serializers.is_valid():
                serializers.save()
                return Response({
                            "status":200,
                            "result":"event create",
                            "data" : serializers.data 
            })
            return Response({"status":400, "error":serializers.errors})
        except Exception as e:
            print(e)
        return Response({"status":500, "message":"something went wrong"})
