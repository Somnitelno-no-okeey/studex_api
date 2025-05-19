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

    interest = models.IntegerField(
        choices=RATING_CHOICES,
        default=0,
        verbose_name="Интересность"
    )
    complexity = models.IntegerField(
        choices=RATING_CHOICES,
        default=0,
        verbose_name="Сложность"
    )
    usefulness = models.IntegerField(
        choices=RATING_CHOICES,
        default=0,
        verbose_name="Полезность"
    )
    workload = models.IntegerField(
        choices=RATING_CHOICES,
        default=0,
        verbose_name="Нагрузка"
    )
    practical_applicability = models.IntegerField(
        choices=RATING_CHOICES,
        default=0,
        verbose_name="Практическая применимость"
    )
    logical_structure = models.IntegerField(
        choices=RATING_CHOICES,
        default=0,
        verbose_name="Логическая структура"
    )
    teaching_effectiveness = models.IntegerField(
        choices=RATING_CHOICES,
        default=0,
        verbose_name="Эффективность преподавания"
    )
    materials_availability = models.IntegerField(
        choices=RATING_CHOICES,
        default=0,
        verbose_name="Доступность материалов"
    )
    feedback_support = models.IntegerField(
        choices=RATING_CHOICES,
        default=0,
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
