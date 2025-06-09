from rest_framework import serializers
from .models import Discipline, Lecturer

class LecturerSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Lecturer
        fields = ['full_name']

    def get_full_name(self, obj):
        return obj.get_full_name()

class DisciplineListSerializer(serializers.ModelSerializer):
    format = serializers.CharField(source='get_format_display')
    control_type = serializers.CharField(source='get_control_type_display')

    class Meta:
        model = Discipline
        fields = [
            'id',
            'name',
            'module',
            'avg_rating',
            'review_count',
            'format',
            'control_type',
        ]

class DisciplineDetailSerializer(serializers.ModelSerializer):
    teachers = LecturerSerializer(many=True)
    format = serializers.CharField(source='get_format_display')
    control_type = serializers.CharField(source='get_control_type_display')
    last_update = serializers.SerializerMethodField()

    class Meta:
        model = Discipline
        fields = [
            'name',
            'module',
            'format',
            'control_type',
            'avg_rating',
            'review_count',
            'teachers',
            'description',
            'last_update',
            'avg_interest',
            'avg_complexity',
            'avg_usefulness',
            'avg_workload',
            'avg_logical_structure',
            'avg_practical_applicability',
            'avg_teaching_effectiveness',
            'avg_materials_availability',
            'avg_feedback_support',
        ]

    def get_last_update(self, obj):
        return obj.updated_at.strftime('%d.%m.%Y')
