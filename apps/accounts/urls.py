from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from apps.accounts.views import RegisterAPIView, ResendVerificationCodeAPIView, VerifyAccountAPIView

urlpatterns = [
    path('', RegisterAPIView.as_view(), name='registration'),
    path('verify/', VerifyAccountAPIView.as_view(), name='verify_account'),
    path('resend-code/', ResendVerificationCodeAPIView.as_view(), name='resend_code'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]