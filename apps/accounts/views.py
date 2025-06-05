from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.permissions import IsAuthenticated
from apps.accounts.models import User
from apps.accounts.serializers import CreateUserSerializer, LoginUserSerializer, PasswordResetConfirmSerializer, PasswordResetRequestSerializer, PasswordResetVerifySerializer, ResendVerificationCodeSerializer, VerifyAccountSerializer, UserSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from apps.accounts.utils import generate_verification_code, send_password_reset_email, send_verification_email

class RegisterAPIView(APIView):
    serializer_class = CreateUserSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': "success"}, status=201)
        return Response(serializer.errors, status=400)
    

class LoginAPIView(APIView):
    @extend_schema(
        request=LoginUserSerializer,
        examples=[
            OpenApiExample(
                'Example request',
                value={
                    'email': 'user@example.com',
                    'password': 'string'
                },
                request_only=True
            )
        ],
    )
    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            response = Response({
                "user": UserSerializer(user).data},
                                status=200)
            
            response.set_cookie(key="access_token", 
                                value=access_token,
                                httponly=True,
                                secure=True,
                                samesite="Lax")
            
            response.set_cookie(key="refresh_token",
                                value=str(refresh),
                                httponly=True,
                                secure=True,
                                samesite="Lax")
            return response
        return Response(serializer.errors, status=400)


class LogoutAPIView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        if refresh_token:
            try:
                refresh = RefreshToken(refresh_token)
                refresh.blacklist()
            except Exception as e:
                return Response({"error":"Error invalidating token:" + str(e) }, status=400)
        
        response = Response({"message": "Successfully logged out!"}, status=200)
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        
        return response    

class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request):
        
        refresh_token = request.COOKIES.get("refresh_token")
        
        if not refresh_token:
            return Response({"error":"Refresh token not provided"}, status= 401)
    
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            
            response = Response({"message": "Access token token refreshed successfully"}, status=200)
            response.set_cookie(key="access_token", 
                                value=access_token,
                                httponly=True,
                                secure=True,
                                samesite="None")
            return response
        except InvalidToken:
            return Response({"error":"Invalid token"}, status=401)
        

class VerifyAccountAPIView(APIView):
    @extend_schema(
        request=VerifyAccountSerializer,
        examples=[
            OpenApiExample(
                'Example request',
                value={
                    'email': 'user@example.com',
                    'verification_code': '123456'
                },
                request_only=True
            )
        ],
    )
    def post(self, request):
        serializer = VerifyAccountSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=400)
        
        email = serializer.validated_data['email']
        user = User.objects.get(email=email)  
        user.is_verificated = True
        user.verification_code = None
        user.save()
        return Response({'message': 'Account verified successfully'}, status=200)


class ResendVerificationCodeAPIView(APIView):
    @extend_schema(
        request=ResendVerificationCodeSerializer,
        examples=[
            OpenApiExample(
                'Example request',
                value={
                    'email': 'user@example.com',
                },
                request_only=True
            )
        ],
    )
    def post(self, request):
        serializer = ResendVerificationCodeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=400)
        
        email = serializer.validated_data['email']
        user = User.objects.get_or_none(email=email)

        if not user.can_send_new_password_reset_code():
            return Response({'error': 'Password reset code can be requested no more than once every 2 minutes.'}, status=400)
        
        user.verification_code = generate_verification_code()
        user.verification_code_sent_at = timezone.now()
        user.save()
        send_verification_email(user.email, user.verification_code)
        return Response({'message': 'A new verification code has been sent to your email.'}, status=200)
    

class PasswordResetRequestAPIView(APIView):
    @extend_schema(
        request=PasswordResetRequestSerializer,
        examples=[
            OpenApiExample(
                'Example request',
                value={
                    'email': 'user@example.com',
                },
                request_only=True
            )
        ],
    )
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=400)
        
        email = serializer.validated_data['email']
        user = User.objects.get(email=email)

        if not user.can_send_new_password_reset_code():
            return Response({'error': 'Password reset code can be requested no more than once every 2 minutes.'}, status=400)
        
        user.password_reset_code = generate_verification_code()
        user.password_reset_code_sent_at = timezone.now()
        user.save()
        send_password_reset_email(user.email, user.password_reset_code)
        return Response({'message': 'Password reset code has been sent to your email.'}, status=200)


class PasswordResetVerifyAPIView(APIView):
    @extend_schema(
        request=PasswordResetVerifySerializer,
        examples=[
            OpenApiExample(
                'Example request',
                value={
                    'email': 'user@example.com',
                    'password_reset_code': '123456'
                },
                request_only=True
            )
        ],
    )
    def post(self, request):
        serializer = PasswordResetVerifySerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=400)
        
        return Response({'message': 'Password reset code is valid'}, status=200)


class PasswordResetConfirmAPIView(APIView):
    @extend_schema(
        request=PasswordResetConfirmSerializer,
        examples=[
            OpenApiExample(
                'Example request',
                value={
                    'email': 'user@example.com',
                    'password_reset_code': '123456',
                    'new_password': 'newpassword'
                },
                request_only=True
            )
        ],
    )
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=400)
        
        serializer.save()
        return Response({'message': 'Password has been reset successfully'}, status=200)