from cgitb import lookup
from django.db.models import query
from markupsafe import re
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework import generics, serializers, status
from rest_framework.views import APIView
from .models import User, CustomersModel, TechniciansModel, \
    TechHasSkillsModel
from .serializers import UserSerializer, CustomersSerializer, \
    TechniciansSerializer


class UserLogin(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request):
        """
        urls: http://127.0.0.1:8000/users/login_user/
        request: {
            "username": "xxxx",
            "password": "pppp"
        }
        return access_token and refresh token
        """
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            token = {
                'token': serializer.validated_data['access'],
                'refresh_token': serializer.validated_data['refresh']
            }
            return Response(
                { 
                    "message": "login user success", 
                    "access_token": token
                }, 
                status=status.HTTP_200_OK)

        return Response(
            {
                "message": "login admin failed", 
                "errors": serializer.errors 
            }, 
            status=status.HTTP_400_BAD_REQUEST
        )


class CustomerCreate(APIView):

    def post(self, request):
        data = request.data
        phone_no = '-'

        if 'phone_no' in data:
            phone_no = data.pop('phone_no')

        user_serializer = UserSerializer(data=data)
        if user_serializer.is_valid():
            user_serializer.save()
            user_id = user_serializer.data.get('id', None)

            customer_data = {"user": user_id, "phone_no": phone_no}
            customer_serializer = CustomersSerializer(data=customer_data)
            if customer_serializer.is_valid():
                customer_serializer.save()
                return Response(
                    {'message': 'create_user success'}, 
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'message': 'create_user failed', 
                        'error': customer_serializer.errors
                    }, 
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(
            {
                'message': 'user failed', 
                'error': user_serializer.errors
            }, 
            status=status.HTTP_400_BAD_REQUEST
        )


class CustomerCrud(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomersModel.objects.all()
    serializer_class = CustomersSerializer

    def filter_queryset(self, queryset):
        id = self.kwargs.get('id', None)

        if id:
            queryset = queryset.filter_id(id)

        return queryset

    def get_object(self):
        id = self.kwargs.get('id', None)
        instance = self.get_queryset().get(id=id)
        return instance
        
    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        data = self.get_serializer(queryset, many=True).data
        
        return Response({'body': data}, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        return serializer.save()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        serializer = self.serializer_class(instance, data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return super().update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        if queryset.exists():
            queryset.delete()
            return Response(
                {'message': 'delete is successful'}, 
                status=status.HTTP_200_OK
            )

        return Response(
            {'error': 'delete is insuccessful'}, 
            status=status.HTTP_404_NOT_FOUND
        )


class TechniciansCrud(generics.RetrieveUpdateDestroyAPIView):
    queryset = TechniciansModel.objects.all()
    serializer_class = TechniciansSerializer
    lookup_field = 'id'
