from rest_framework import serializers
from apps.reviews.models import Review

class CriterionSerializer(serializers.Serializer):
    criterion = serializers.CharField()
    rating = serializers.FloatField()

class ReviewListSerializer(serializers.ModelSerializer):
    is_user_review = serializers.SerializerMethodField()
    student_name = serializers.SerializerMethodField()
    published_at = serializers.DateField(source='created_at', format='%Y-%m-%d')
    average_rating = serializers.SerializerMethodField()
    criteria = serializers.SerializerMethodField()
    text = serializers.CharField(source='review_text')

    class Meta:
        model = Review
        fields = [
            'id',
            'is_user_review',
            'student_name',
            'published_at',
            'average_rating',
            'criteria',
            'text',
        ]

    def get_is_user_review(self, obj):
        user = self.context['request'].user
        return obj.user == user

    def get_student_name(self, obj):
        if obj.is_anonymous:
            return "Аноним"
        return f"{obj.user.first_name} {obj.user.last_name}".strip()

    def get_average_rating(self, obj):
        ratings = self._get_ratings_list(obj)
        valid_ratings = [r for r in ratings if r is not None]
        if not valid_ratings:
            return None
        return round(sum(valid_ratings) / len(valid_ratings), 1)

    def get_criteria(self, obj):
        mapping = {
            'avg_interest': "Интересность дисциплины",
            'avg_complexity': "Уровень сложности",
            'avg_usefulness': "Полезность содержания",
            'avg_workload': "Объем нагрузки",
            'avg_logical_structure': "Логичность структуры",
            'avg_practical_applicability': "Практическая применимость",
            'avg_teaching_effectiveness': "Эффективность преподавания",
            'avg_materials_availability': "Доступность учебных материалов",
            'avg_feedback_support': "Обратная связь и поддержка",
        }

        criteria = []
        for field, label in mapping.items():
            rating = getattr(obj, field)
            if rating is not None:
                criteria.append({
                    "criterion": label,
                    "rating": round(rating, 1)
                })
        return criteria

    def _get_ratings_list(self, obj):
        return [
            obj.avg_interest,
            obj.avg_complexity,
            obj.avg_usefulness,
            obj.avg_workload,
            obj.avg_logical_structure,
            obj.avg_practical_applicability,
            obj.avg_teaching_effectiveness,
            obj.avg_materials_availability,
            obj.avg_feedback_support
        ]

    def get_fields(self):
        fields = super().get_fields()
        fields['criteria'] = serializers.ListSerializer(child=CriterionSerializer())
        return fields
