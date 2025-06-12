from django.urls import path
from apps.accounts.views import CookieTokenRefreshView, LoginAPIView, LogoutAPIView, PasswordResetConfirmAPIView, PasswordResetRequestAPIView, PasswordResetVerifyAPIView, RegisterAPIView, ResendVerificationCodeAPIView, VerifyAccountAPIView, UserProfileAPIView, UpdateFullNameAPIView, ChangePasswordAPIView

urlpatterns = [
    path("profile/", UserProfileAPIView.as_view(), name="user-profile"),
    path('registration/', RegisterAPIView.as_view(), name='registration'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),

    path('refresh/', CookieTokenRefreshView.as_view(), name='refresh'),

    path('verify/', VerifyAccountAPIView.as_view(), name='verify_account'),
    path('verify/resend-code/', ResendVerificationCodeAPIView.as_view(), name='resend_code'),

    path('password-reset/request/', PasswordResetRequestAPIView.as_view(), name='password-reset-request'),
    path('password-reset/verify/', PasswordResetVerifyAPIView.as_view(), name='password-reset-verify'),
    path('password-reset/confirm/', PasswordResetConfirmAPIView.as_view(), name='password-reset-confirm'),
    path('update-fullname/', UpdateFullNameAPIView.as_view(), name='update-fullname'),
    path('change-password/', ChangePasswordAPIView.as_view(), name='change-password'),
]
