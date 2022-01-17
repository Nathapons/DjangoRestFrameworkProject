from .models import ServiceModel
from rest_framework import generics
from .serializers import ServiceListSerializer


class ServiceList(generics.ListAPIView):
    queryset = ServiceModel.objects.all()
    serializer_class = ServiceListSerializer
    