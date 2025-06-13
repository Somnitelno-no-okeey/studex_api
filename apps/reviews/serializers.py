from rest_framework import serializers
from .models import Review
from apps.disciplines.models import Discipline


BAD_WORDS = ["badword1", "badword2", "плохое_слово"]  # потом нужно будет добавить их

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ('user',)

    def validate(self, data):
        discipline = self.context['discipline']

        # Проверка обязательных полей
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

        comment = data.get('comment', '').lower()
        if any(bad_word in comment for bad_word in BAD_WORDS):
            raise serializers.ValidationError({"comment": "Комментарий содержит недопустимые слова."})

        return data

class ReviewListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            'id', 'user', 'interest', 'complexity', 'usefulness', 'workload',
            'logical_structure', 'practical_applicability',
            'teaching_effectiveness', 'materials_availability', 'feedback_support',
            'comment', 'anonymous', 'created_at'
        ]

    def get_user(self, obj):
        return "Аноним" if obj.anonymous else obj.user.username