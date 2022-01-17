from rest_framework import serializers 


class ServiceListSerializer(serializers.Serializer):
    category = serializers.CharField(source='category.name', read_only=True)
    service = serializers.CharField(read_only=True)
    price = serializers.DecimalField(max_digits=99, decimal_places=2, read_only=True)
