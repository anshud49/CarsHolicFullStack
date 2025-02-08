from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from .models import CarModel, CarImage
from .serializers import CarModelSerializer, CarImageSerializer, UserRegistrationSerializer,LoginSerializer
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny,IsAuthenticatedOrReadOnly
from django.contrib.auth.models import AnonymousUser
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from google.auth.transport.requests import Request
from google.oauth2 import id_token
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes


@api_view(['POST'])
@permission_classes([AllowAny])
def google_login(request):
    token = request.data.get('token')
    if not token:
        return Response({'error': 'Token is required'}, status=400)

    try:
        idinfo = id_token.verify_oauth2_token(token, Request(), '77147079337-el3d08s5o5h305bcj27me9iv5qjddiu7.apps.googleusercontent.com')
        email = idinfo['email']
        name = idinfo.get('name', '')

        user, created = User.objects.get_or_create(email=email, defaults={'username': email})

        if created:
            user.username = email
            user.first_name = name  
            user.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        })

    except ValueError:
        return Response({'error': 'Invalid Google token'}, status=400)
    except Exception as e:
        return Response({'error': str(e)}, status=400)


def Docs(request):
    return render(request, 'docs.html')

class UserRegistrationView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer


class UserLoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer  

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)



class UserLogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try: 
            refresh_token = request.data.get('refresh_token')
            
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({"message": "Successfully logged out"}, status=status.HTTP_205_RESET_CONTENT)
            else:
                return Response({"error": "Refresh token is required for logout"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
           
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class CarModelViewSet(viewsets.ModelViewSet):
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer
    permission_classes=[IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        
        if isinstance(user, AnonymousUser):
            return CarModel.objects.filter(public=True)

        is_logged_in = self.request.query_params.get("isLoggedin", None)

        if is_logged_in is not None:
            if is_logged_in.lower() == "true":
                return CarModel.objects.filter(public=True).exclude(user=user)
        else:
            return CarModel.objects.filter(user=user)


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        images_data = request.data.get('images', [])
        logo_url = request.data.get('logo_url', None)

        car_serializer = self.get_serializer(data=request.data)
        car_serializer.is_valid(raise_exception=True)
        car = car_serializer.save()

        if logo_url:
            car.logo_url = logo_url
            car.save()

        if images_data:
            for image_url in images_data[:10]: 
                CarImage.objects.create(car=car, image_url=image_url, user=request.user)

        headers = self.get_success_headers(car_serializer.data)
        return Response(car_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        images_data = request.data.get('images', [])
        logo_url = request.data.get('logo_url', None)
        
        car_serializer = self.get_serializer(instance, data=request.data, partial=False)
        car_serializer.is_valid(raise_exception=True)
        car = car_serializer.save()

        if logo_url:
            car.logo_url = logo_url
            car.save()

        if images_data:
            car.images.all().delete()
            for image_url in images_data[:10]:
                CarImage.objects.create(car=car, image_url=image_url, user=request.user)

        headers = self.get_success_headers(car_serializer.data)
        return Response(car_serializer.data, status=status.HTTP_200_OK, headers=headers)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        images_data = request.data.get('images', [])
        logo_url = request.data.get('logo_url', None)

        car_serializer = self.get_serializer(instance, data=request.data, partial=True)
        car_serializer.is_valid(raise_exception=True)
        car = car_serializer.save()

        if logo_url:
            car.logo_url = logo_url
            car.save()

        if images_data:
            car.images.all().delete()
            for image_url in images_data[:10]:
                CarImage.objects.create(car=car, image_url=image_url, user=request.user)

        headers = self.get_success_headers(car_serializer.data)
        return Response(car_serializer.data, status=status.HTTP_200_OK, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class CarImageViewSet(viewsets.ModelViewSet):
    queryset = CarImage.objects.all()
    serializer_class = CarImageSerializer

   
    def perform_create(self, serializer):
        car_id = self.request.data.get('car')
        image_url = self.request.data.get('image_url')  
        if car_id and CarModel.objects.filter(id=car_id).exists():
            car = CarModel.objects.get(id=car_id)
            if car.images.count() < 10:
                
                serializer.save(car=car, image_url=image_url, user=self.request.user) 
            else:
                raise serializers.ValidationError("A car can have a maximum of 10 images.")
        else:
            raise serializers.ValidationError("Car ID is required or invalid.")
    
    @action(detail=True, methods=['post'])
    def add_images(self, request, pk=None):
        car = self.get_object()
        if car.images.count() >= 10:
            return Response({"detail": "A car can have a maximum of 10 images."}, status=400)

        images = request.data.get('images', [])
        for image_url in images:
            CarImage.objects.create(car=car, image_url=image_url, user=request.user)
        return Response({"detail": "Images added successfully."}, status=201)
    
    def destroy(self, request, *args, **kwargs):
        try:
            image = self.get_object() 
            if image.user != request.user:
                return Response({"detail": "You do not have permission to delete this image."}, status=403)
            image.delete()
            return Response({"detail": "Image deleted successfully."}, status=204)
        except Exception as e:
            return Response({"detail": str(e)}, status=400)
        

    