from rest_framework import serializers
from .models import CarModel, CarImage
from django.contrib.auth.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True)


class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ['id', 'image_url']  

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)



class CarModelSerializer(serializers.ModelSerializer):
    images = CarImageSerializer(many=True, read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = CarModel
        fields = ['id', 'car_name', 'description', 'tags', 'title', 'car_type', 'company', 'dealer', 'logo_url', 'images', 'user','public']

    def validate_car_name(self, value):
        user = self.context['request'].user 
        car_instance = self.instance

       
        if car_instance and car_instance.car_name == value:
            return value  

       
        if CarModel.objects.filter(car_name=value, user=user).exists():
            raise serializers.ValidationError("You already have a car with this name.")
        
        return value

