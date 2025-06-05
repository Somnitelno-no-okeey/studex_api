from django.db import models
from apps.accounts.models import User
from apps.common.models import IsDeletedModel
from apps.disciplines.models import Discipline


RATING_CHOICES = [(i, str(i)) for i in range(6)]


class Review(IsDeletedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, related_name='reviews')
    review_text = models.TextField(verbose_name='Текст отзыва')
    is_anonymous = models.BooleanField(default=False, verbose_name='Анонимность')

    avg_interest = models.FloatField(
        null=True, 
        default=None, 
        verbose_name="Интересность дисциплины"
    )
    avg_complexity = models.FloatField(
        null=True, 
        default=None,
        verbose_name="Уровень сложности"
    )
    avg_usefulness = models.FloatField(
        null=True, 
        default=None, 
        verbose_name="Полезность содержания"
    )
    avg_workload = models.FloatField(
        null=True, 
        default=None, 
        verbose_name="Объем нагрузки"
    )
    avg_logical_structure = models.FloatField(
        null=True, 
        default=None, 
        verbose_name="Логичность структуры"
    )
    avg_practical_applicability = models.FloatField(
        null=True, 
        default=None, 
        verbose_name="Практическая применимость"
    )
    avg_teaching_effectiveness = models.FloatField(
        null=True, 
        default=None, 
        verbose_name="Эффективность преподавания"
    )
    avg_materials_availability = models.FloatField(
        null=True, 
        default=None, 
        verbose_name="Доступность учебных материалов"
    )
    avg_feedback_support = models.FloatField(
        null=True, 
        default=None, 
        verbose_name="Обратная связь и поддержка"
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"Отзыв от {self.user} для {self.discipline}"
