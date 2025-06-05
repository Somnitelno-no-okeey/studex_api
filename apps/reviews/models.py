from django.db import models
from apps.accounts.models import User
from apps.common.models import IsDeletedModel
from apps.disciplines.models import Discipline


RATING_CHOICES = (
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10')
    )



class Review(IsDeletedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, related_name='reviews')
    review_text = models.TextField(verbose_name='Текст отзыва')
    is_anonymous = models.BooleanField(default=False, verbose_name='Анонимность')
    ai_evaluation = models.IntegerField(verbose_name='Оценка отзыва нейросетью')

    avg_interest = models.FloatField(
        default=None,
        verbose_name="Интересность дисциплины"
    )
    avg_complexity = models.FloatField(
        default=None,
        verbose_name="Уровень сложности"
    )
    avg_usefulness = models.FloatField(
        default=None,
        verbose_name="Полезность содержания"
    )
    avg_workload = models.FloatField(
        default=None,
        verbose_name="Объем нагрузки"
    )
    avg_logical_structure = models.FloatField(
        default=None,
        verbose_name="Логичность структуры"
    )
    avg_practical_applicability = models.FloatField(
        default=None,
        verbose_name="Практическая применимость"
    )
    avg_teaching_effectiveness = models.FloatField(
        default=None,
        verbose_name="Эффективность преподавания"
    )
    avg_materials_availability = models.FloatField(
        default=None,
        verbose_name="Доступность учебных материалов"
    )
    avg_feedback_support = models.FloatField(
        default=None,
        verbose_name="Обратная связь и поддержка"
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"



class Comment(IsDeletedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    comment_text = models.TextField(verbose_name='Текст комментария')

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
