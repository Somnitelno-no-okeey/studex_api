from django.db import models
from apps.common.models import BaseModel
from django.db.models import Avg

FORMAT_TYPE_CHOICES = (
    ('TRADITIONAL', 'TRADITIONAL'),
    ('ONLINE', 'ONLINE'),
    ('BLENDED', 'BLENDED')
)


class Discipline(BaseModel):
    name = models.CharField(max_length=255, verbose_name='Название дисциплины')
    description = models.TextField(verbose_name='Описание дисциплины')
    module = models.CharField(max_length=100, verbose_name='Модуль')
    format = models.CharField(max_length=11, choices=FORMAT_TYPE_CHOICES, default='TRADITIONAL', verbose_name='Формат проведения')
    
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
        verbose_name = "Дисциплина"
        verbose_name_plural = "Дисциплины" 

    
class Lecturer(BaseModel):
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=150, verbose_name='Отчество')
    disciplines = models.ManyToManyField(Discipline, related_name='lecturers')
    
    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"