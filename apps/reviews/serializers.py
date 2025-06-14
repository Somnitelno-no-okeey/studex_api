from rest_framework import serializers
from .models import Review

BAD_WORDS = ["badword1", "badword2", "плохое_слово"]

CRITERIA_MAPPING = {
    'interest': 'Интересность дисциплины',
    'complexity': 'Уровень сложности', 
    'usefulness': 'Полезность содержания',
    'workload': 'Объем нагрузки',
    'logical_structure': 'Логичность структуры',
    'practical_applicability': 'Практическая применимость',
    'teaching_effectiveness': 'Эффективность преподавания',
    'materials_availability': 'Доступность учебных материалов',
    'feedback_support': 'Обратная связь и поддержка',
}

REVERSE_CRITERIA_MAPPING = {v: k for k, v in CRITERIA_MAPPING.items()}


class ReviewSerializer(serializers.ModelSerializer):
    criteria = serializers.ListField(child=serializers.DictField(), write_only=True)

    class Meta:
        model = Review
        fields = ['criteria', 'comment', 'anonymous']
        read_only_fields = ['average', 'user', 'discipline']

    def validate(self, data):
        discipline = self.context['discipline']
        criteria_data = data.pop('criteria', [])
        
        criteria_dict = {}
        for item in criteria_data:
            criterion_verbose = item['criterion']
            if criterion_verbose not in REVERSE_CRITERIA_MAPPING:
                raise serializers.ValidationError({"criteria": f"Неизвестный критерий: {criterion_verbose}"})
            field_name = REVERSE_CRITERIA_MAPPING[criterion_verbose]
            criteria_dict[field_name] = item['rating']
        
        required_fields = ['interest', 'complexity']
        for field in required_fields:
            if field not in criteria_dict:
                raise serializers.ValidationError({field: f"Обязательное поле: {CRITERIA_MAPPING[field]}"})
            if not (1 <= criteria_dict[field] <= 5):
                raise serializers.ValidationError({field: "Оценка обязательна от 1 до 5."})
        
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
            if field in criteria_dict and not is_active:
                raise serializers.ValidationError({"criteria": f"Критерий '{CRITERIA_MAPPING[field]}' неактивен для этой дисциплины"})
            if is_active:
                if field not in criteria_dict:
                    raise serializers.ValidationError({field: f"Обязательное поле: {CRITERIA_MAPPING[field]}"})
                if not (1 <= criteria_dict[field] <= 5):
                    raise serializers.ValidationError({field: "Обязательное поле: оценка от 1 до 5."})
        
        user = self.context['request'].user
        if self.instance is None:
            if Review.objects.filter(user=user, discipline=discipline).exists():
                raise serializers.ValidationError("Вы уже оставляли отзыв на эту дисциплину")
        
        for field, rating in criteria_dict.items():
            data[field] = rating
            data[f'is_{field}_active'] = True
        
        for field in active_fields:
            if field not in criteria_dict:
                data[f'is_{field}_active'] = False
        
        data['is_interest_active'] = True
        data['is_complexity_active'] = True

        comment = data.get('comment', '') or ''
        if any(bad_word in comment.lower() for bad_word in BAD_WORDS):
            raise serializers.ValidationError({"comment": "Комментарий содержит недопустимые выражения."})

        return data


class ReviewListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    criteria = serializers.SerializerMethodField()
    avg_rating = serializers.FloatField(read_only=True)
    created_at = serializers.DateTimeField(format="%d.%m.%Y", read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'criteria', 'comment', 'created_at', 'avg_rating']

    def get_user(self, obj):
        return "Аноним" if obj.anonymous else obj.user.get_full_name()

    def get_criteria(self, obj):
        discipline = obj.discipline
        criteria = []

        fields = [
            ('interest', True),
            ('complexity', True),
            ('usefulness', discipline.is_usefulness_active),
            ('workload', discipline.is_workload_active),
            ('logical_structure', discipline.is_logical_structure_active),
            ('practical_applicability', discipline.is_practical_applicability_active),
            ('teaching_effectiveness', discipline.is_teaching_effectiveness_active),
            ('materials_availability', discipline.is_materials_availability_active),
            ('feedback_support', discipline.is_feedback_support_active),
        ]

        for field_name, is_active in fields:
            if is_active:
                criteria.append({
                    "criterion": CRITERIA_MAPPING[field_name],
                    "rating": getattr(obj, field_name)
                })

        return criteria