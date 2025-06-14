from rest_framework import serializers
from .models import Review

BAD_WORDS = ["badword1", "badword2", "плохое_слово"] # потом нужно будет добавить их


class CriteriaSerializer(serializers.Serializer):
    name = serializers.CharField()
    rating = serializers.IntegerField(min_value=1, max_value=5)


class ReviewSerializer(serializers.ModelSerializer):
    criteria = serializers.SerializerMethodField()

    class Meta:
        model = Review
        exclude = ('user',)

    def get_criteria(self, obj):
        discipline = obj.discipline
        criteria = []

        fields = [
            ('interest', getattr(discipline, 'is_interest_active', True)),
            ('complexity', getattr(discipline, 'is_complexity_active', True)),
            ('usefulness', getattr(discipline, 'is_usefulness_active', True)),
            ('workload', getattr(discipline, 'is_workload_active', True)),
            ('logical_structure', getattr(discipline, 'is_logical_structure_active', True)),
            ('practical_applicability', getattr(discipline, 'is_practical_applicability_active', True)),
            ('teaching_effectiveness', getattr(discipline, 'is_teaching_effectiveness_active', True)),
            ('materials_availability', getattr(discipline, 'is_materials_availability_active', True)),
            ('feedback_support', getattr(discipline, 'is_feedback_support_active', True)),
        ]

        for field_name, is_active in fields:
            if is_active:
                criteria.append({"name": field_name, "rating": getattr(obj, field_name)})

        return criteria

    def validate(self, data):
        discipline = self.context['discipline']

        if not (1 <= data.get('interest', 0) <= 5):
            raise serializers.ValidationError({"interest": "Оценка обязательна от 1 до 5."})
        if not (1 <= data.get('complexity', 0) <= 5):
            raise serializers.ValidationError({"complexity": "Оценка обязательна от 1 до 5."})

        active_fields = {
            'usefulness': discipline.is_usefulness_active,
            'workload': discipline.is_workload_active,
            'logical_structure': discipline.is_logical_structure_active,
            'practical_applicability': discipline.is_practical_applicability_active,
            'teaching_effectiveness': discipline.is_teaching_effectiveness_active,
            'materials_availability': discipline.is_materials_availability_active,
            'feedback_support': discipline.is_feedback_support_active,
        }
        for field, is_active in active_fields.items():
            if is_active and not (1 <= data.get(field, 0) <= 5):
                raise serializers.ValidationError({field: "Обязательное поле: оценка от 1 до 5."})

        comment = data.get('comment', '') or ''
        if any(bad_word in comment.lower() for bad_word in BAD_WORDS):
            raise serializers.ValidationError({"comment": "Комментарий содержит недопустимые выражения."})

        return data


class ReviewListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    criteria = CriteriaSerializer(many=True, read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'criteria', 'comment', 'anonymous', 'created_at']

    def get_user(self, obj):
        return "Аноним" if obj.anonymous else obj.user.username

    def get_criteria(self, obj):
        discipline = obj.discipline
        criteria = []

        fields = [
            ('interest', getattr(discipline, 'is_interest_active', True)),
            ('complexity', getattr(discipline, 'is_complexity_active', True)),
            ('usefulness', getattr(discipline, 'is_usefulness_active', True)),
            ('workload', getattr(discipline, 'is_workload_active', True)),
            ('logical_structure', getattr(discipline, 'is_logical_structure_active', True)),
            ('practical_applicability', getattr(discipline, 'is_practical_applicability_active', True)),
            ('teaching_effectiveness', getattr(discipline, 'is_teaching_effectiveness_active', True)),
            ('materials_availability', getattr(discipline, 'is_materials_availability_active', True)),
            ('feedback_support', getattr(discipline, 'is_feedback_support_active', True)),
        ]

        for field_name, is_active in fields:
            if is_active:
                criteria.append({"criterion": field_name, "rating": getattr(obj, field_name)})

        return criteria
