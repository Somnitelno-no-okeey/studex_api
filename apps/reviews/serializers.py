from rest_framework import serializers
from apps.reviews.models import Review
from apps.accounts.models import User
from apps.disciplines.models import Discipline

class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']

class DisciplineShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = ['id', 'name', 'module']

class ReviewListSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)
    discipline = DisciplineShortSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id',
            'user',
            'discipline',
            'review_text',
            'is_anonymous',
            'ai_evaluation',
            'interest',
            'complexity',
            'usefulness',
            'workload',
            'practical_applicability',
            'logical_structure',
            'teaching_effectiveness',
            'materials_availability',
            'feedback_support',
            'created_at',
            'updated_at'
        ]