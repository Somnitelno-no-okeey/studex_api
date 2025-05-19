from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from apps.accounts.models import User
from apps.accounts.utils import generate_verification_code, send_verification_email


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')

    def create(self, validated_data):
        email = validated_data['email']
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'password': make_password(validated_data['password']),
                'verification_code': generate_verification_code(),
                'verification_code_sent_at': timezone.now()
            }
        )
        
        if not created:
            user.verification_code = generate_verification_code()
            user.verification_code_sent_at = timezone.now()
            user.save()
        
        send_verification_email(user.email, user.verification_code)
        return user
    
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields =("id", "email")


class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        user = authenticate(**data)
        if user:
            return user
        raise serializers.ValidationError("Incorrect credentinls")

class VerifyAccountSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    verification_code = serializers.CharField(required=True, max_length=6)

    def validate(self, data):
        email = data['email']
        verification_code = data['verification_code']
        
        user = User.objects.filter(email=email).first()
        
        if not user:
            raise serializers.ValidationError({"email": "User with this email does not exist."})
        if user.is_verificated:
            raise serializers.ValidationError({"email": "Account is already verified"})
        if user.verification_code != verification_code:
            raise serializers.ValidationError({"verification_code": "Invalid verification code"})
            
        return data


class ResendVerificationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    def validate(self, data):
        email = data['email']
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "User with this email does not exist."})
        return data


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, data):
        email = data['email']
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "User with this email does not exist."})
        return data


class PasswordResetVerifySerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password_reset_code = serializers.CharField(required=True, max_length=6)

    def validate(self, data):
        email = data['email']
        password_reset_code = data['password_reset_code']
        
        user = User.objects.filter(email=email).first()
        
        if not user:
            raise serializers.ValidationError({"email": "User with this email does not exist."})
        if user.password_reset_code != password_reset_code:
            raise serializers.ValidationError({"password_reset_code": "Invalid password reset code"})
            
        return data


class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password_reset_code = serializers.CharField(required=True, max_length=6)
    new_password = serializers.CharField(required=True, min_length=8)

    def validate(self, data):
        email = data['email']
        password_reset_code = data['password_reset_code']
        
        user = User.objects.filter(email=email).first()
        
        if not user:
            raise serializers.ValidationError({"email": "User with this email does not exist."})
        if user.password_reset_code != password_reset_code:
            raise serializers.ValidationError({"password_reset_code": "Invalid password reset code"})
            
        return data

    def save(self):
        user = User.objects.get(email=self.validated_data['email'])
        user.password = make_password(self.validated_data['new_password'])
        user.password_reset_code = None
        user.save()
