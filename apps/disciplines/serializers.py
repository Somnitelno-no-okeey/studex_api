from rest_framework import serializers
from .models import Discipline, Lecturer


class LecturerSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Lecturer
        fields = ['full_name']

    def get_full_name(self, obj):
        return obj.get_full_name()


class DisciplineCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = [
            'name',
            'module',
            'format',
            'control_type',
            'description',
            'teachers',

            'avg_interest',
            'avg_complexity',
            'avg_usefulness',
            'is_usefulness_active',
            'avg_workload',
            'is_workload_active',
            'avg_logical_structure',
            'is_logical_structure_active',
            'avg_practical_applicability',
            'is_practical_applicability_active',
            'avg_teaching_effectiveness',
            'is_teaching_effectiveness_active',
            'avg_materials_availability',
            'is_materials_availability_active',
            'avg_feedback_support',
            'is_feedback_support_active',
        ]


class DisciplineListSerializer(serializers.ModelSerializer):
    module = serializers.StringRelatedField()
    format = serializers.CharField(source='get_format_display')
    control_type = serializers.CharField(source='get_control_type_display')

    class Meta:
        model = Discipline
        fields = [
            'id',
            'name',
            'module',
            'format',
            'control_type',
            'avg_rating',
            'review_count',
        ]


class DisciplineDetailSerializer(serializers.ModelSerializer):
    teachers = LecturerSerializer(many=True)
    format = serializers.CharField(source='get_format_display')
    control_type = serializers.CharField(source='get_control_type_display')
    module = serializers.StringRelatedField()
    last_update = serializers.SerializerMethodField()
    criteria = serializers.SerializerMethodField()

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
            'criteria',
        ]

    def get_last_update(self, obj):
        return obj.updated_at.strftime('%d.%m.%Y') if obj.updated_at else None

    def get_criterion(self, obj, field_name, flag_name=None):
        value = getattr(obj, field_name)
        label = obj._meta.get_field(field_name).verbose_name
        if flag_name:
            active = getattr(obj, flag_name)
            if not active:
                return None
        return {"criterion": label, "rating": value}

    def get_criteria(self, obj):
        criteria = [
            self.get_criterion(obj, 'avg_interest'),
            self.get_criterion(obj, 'avg_complexity'),
            self.get_criterion(obj, 'avg_usefulness', 'is_usefulness_active'),
            self.get_criterion(obj, 'avg_workload', 'is_workload_active'),
            self.get_criterion(obj, 'avg_logical_structure', 'is_logical_structure_active'),
            self.get_criterion(obj, 'avg_practical_applicability', 'is_practical_applicability_active'),
            self.get_criterion(obj, 'avg_teaching_effectiveness', 'is_teaching_effectiveness_active'),
            self.get_criterion(obj, 'avg_materials_availability', 'is_materials_availability_active'),
            self.get_criterion(obj, 'avg_feedback_support', 'is_feedback_support_active'),
        ]

        return [item for item in criteria if item is not None]
