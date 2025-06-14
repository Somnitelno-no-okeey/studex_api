from django.db import models
from apps.common.models import BaseModel
from apps.accounts.models import User
from django.contrib.auth import get_user_model
from apps.disciplines.models import Discipline


User = get_user_model()

class Review(BaseModel):
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, related_name='reviews',
                                   verbose_name='Дисциплина')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')

    interest = models.PositiveSmallIntegerField(default=0, verbose_name='Интересность дисциплины')
    is_interest_active = models.BooleanField(default=False, verbose_name='Учитывать интерес')

    complexity = models.PositiveSmallIntegerField(default=0, verbose_name='Уровень сложности')
    is_complexity_active = models.BooleanField(default=False, verbose_name='Учитывать сложность')

    usefulness = models.PositiveSmallIntegerField(default=0, verbose_name='Полезность содержания')
    is_usefulness_active = models.BooleanField(default=False, verbose_name='Учитывать полезность')

    workload = models.PositiveSmallIntegerField(default=0, verbose_name='Объем нагрузки')
    is_workload_active = models.BooleanField(default=False, verbose_name='Учитывать нагрузку')

    logical_structure = models.PositiveSmallIntegerField(default=0, verbose_name='Логичность структуры')
    is_logical_structure_active = models.BooleanField(default=False, verbose_name='Учитывать логичность структуры')

    practical_applicability = models.PositiveSmallIntegerField(default=0, verbose_name='Практическая применимость')
    is_practical_applicability_active = models.BooleanField(default=False, verbose_name='Учитывать практическое применение')

    teaching_effectiveness = models.PositiveSmallIntegerField(default=0, verbose_name='Эффективность преподавания')
    is_teaching_effectiveness_active = models.BooleanField(default=False, verbose_name='Учитывать эффективность преподавания')

    materials_availability = models.PositiveSmallIntegerField(default=0, verbose_name='Доступность учебных материалов')
    is_materials_availability_active = models.BooleanField(default=False, verbose_name='Учитывать доступность учебных материалов')

    feedback_support = models.PositiveSmallIntegerField(default=0, verbose_name='Обратная связь и поддержка')
    is_feedback_support_active = models.BooleanField(default=False, verbose_name='Учитывать обратную связь и поддержку')

    comment = models.TextField(blank=True, verbose_name='Комментарий')
    anonymous = models.BooleanField(default=False, verbose_name='Анонимно')

    avg_rating = models.FloatField(default=None, null=True, verbose_name='Общая оценка')

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"Отзыв {self.pk} пользователя {self.user} на {self.discipline}" 
