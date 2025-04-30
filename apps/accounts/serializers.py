from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from apps.accounts.models import User
from apps.accounts.utils import can_send_new_code, generate_verification_code, send_verification_email


class CreateUserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'confirm_password')

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "The passwords do not match"})
        return data

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
    