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
    criteria = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'user', 'criteria', 'comment', 'anonymous', 'created_at']

    def get_user(self, obj):
        return "Аноним" if obj.anonymous else obj.user.get_full_name()

    def get_criterion(self, obj, field_name, flag_name=None):
        label = Review._meta.get_field(field_name).verbose_name
        value = getattr(obj, field_name)
        discipline = obj.discipline
        if flag_name:
            is_active = getattr(discipline, flag_name)
            if not is_active:
                return None
        return {"criterion": label, "rating": value}

    def get_criteria(self, obj):
        criteria = [
            self.get_criterion(obj, 'interest'),
            self.get_criterion(obj, 'complexity'),
            self.get_criterion(obj, 'usefulness', 'is_usefulness_active'),
            self.get_criterion(obj, 'workload', 'is_workload_active'),
            self.get_criterion(obj, 'logical_structure', 'is_logical_structure_active'),
            self.get_criterion(obj, 'practical_applicability', 'is_practical_applicability_active'),
            self.get_criterion(obj, 'teaching_effectiveness', 'is_teaching_effectiveness_active'),
            self.get_criterion(obj, 'materials_availability', 'is_materials_availability_active'),
            self.get_criterion(obj, 'feedback_support', 'is_feedback_support_active'),
        ]

        return [item for item in criteria if item is not None]
