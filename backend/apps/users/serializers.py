from rest_framework import serializers
from .models import User, CustomersModel, TechHasSkillsModel, TechniciansModel


class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.set_password(validated_data.get('password', instance.password))

        return instance

    class Meta:
        model = User
        fields = '__all__'


class CustomersSerializer(serializers.ModelSerializer):
    # ModelSerializer => จะ export ออกมาเหมือน model ที่ class Meta ได้กำหนดกไว้
    id = serializers.ReadOnlyField()
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    phone = serializers.ReadOnlyField()

    def create(self, validated_data):
        customer = CustomersModel.object.create(
            **validated_data
        )
        return customer

    def update(self, instance, validated_data):
        instance.phone_no = validated_data.get('phone_no', instance.phone_no)
        return instance

    class Meta:
        model = CustomersModel
        fields = '__all__'


class TechniciansSerializer(CustomersSerializer):

    class Mata:
        model = TechniciansModel
        fields = '__all__'
