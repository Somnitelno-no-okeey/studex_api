from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.accounts.models import User
from apps.accounts.serializers import CreateUserSerializer, ResendVerificationCodeSerializer, VerifyAccountSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from apps.accounts.utils import can_send_new_code, generate_verification_code, send_verification_email


class RegisterAPIView(APIView):
    serializer_class = CreateUserSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': "success"}, status=201)
        return Response(serializer.errors, status=400)
    

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

        if not can_send_new_code(user):
            return Response({'error': 'The verification code can be requested no more than once every 2 minutes.'}, status=400)
        
        user.verification_code = generate_verification_code()
        user.verification_code_sent_at = timezone.now()
        user.save()
        send_verification_email(user.email, user.verification_code)
        return Response({'message': 'A new verification code has been sent to your email.'}, status=200)
