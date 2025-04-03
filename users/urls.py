from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserCreateView, UserDetailView, CustomTokenObtainPairView, LogoutView

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
    path('user/', UserDetailView.as_view(), name='user-detail'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
]