from django.urls import path, include
from rest_framework.routers import DefaultRouter
from CAR.views import Docs,CarModelViewSet,google_login, CarImageViewSet, UserRegistrationView, UserLoginView, UserLogoutView

router = DefaultRouter()
router.register(r'cars', CarModelViewSet, basename='carmodel')
router.register(r'carimages', CarImageViewSet, basename='carimages')

urlpatterns = [
    path('', include(router.urls)),  
    path('auth/google/', google_login, name='google_login'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),
    path('docs/',Docs),
]
