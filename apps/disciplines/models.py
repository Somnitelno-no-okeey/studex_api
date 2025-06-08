from django.db import models
from apps.common.models import BaseModel
from enum import Enum


class DisciplineFormat(models.TextChoices):
    TRADITIONAL = 'TRADITIONAL', 'Традиционная'
    ONLINE = 'ONLINE', 'Онлайн'
    BLENDED = 'BLENDED', 'Смешанная'


class ControlType(models.TextChoices):
    EXAM = 'EXAM', 'Экзамен'
    CREDIT = 'CREDIT', 'Зачет'

class Lecturer(BaseModel):
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=150, verbose_name='Отчество')

    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.patronymic}"
    
class Module(BaseModel):
    name = models.CharField(max_length=100, verbose_name='Название модуля')

    class Meta:
        verbose_name = "Модуль"
        verbose_name_plural = "Модули"

    def __str__(self):
        return self.name

class Discipline(BaseModel):
    name = models.CharField(max_length=255, verbose_name='Название дисциплины')
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='disciplines',
        verbose_name='Модуль'
    )
    avg_rating = models.FloatField(
        default=None,
        null=True,
        blank=True,
        verbose_name='Общая оценка'
    )
    
    format = models.CharField(
        max_length=11,
        choices=DisciplineFormat.choices,
        blank=True,
        verbose_name='Формат проведения'
    )
    control_type = models.CharField(
        max_length=10,
        choices=ControlType.choices,
        blank=True,
        verbose_name='Тип контроля'
    )
    
    avg_interest = models.FloatField(
        default=None,
        null=True,
        verbose_name="Интересность дисциплины"
    )
    avg_complexity = models.FloatField(
        default=None,
        null=True,
        verbose_name="Уровень сложности"
    )
    avg_usefulness = models.FloatField(
        default=None,
        null=True,
        verbose_name="Полезность содержания"
    )
    avg_workload = models.FloatField(
        default=None,
        null=True,
        verbose_name="Объем нагрузки"
    )
    avg_logical_structure = models.FloatField(
        default=None,
        null=True,
        verbose_name="Логичность структуры"
    )
    avg_practical_applicability = models.FloatField(
        default=None,
        null=True,
        verbose_name="Практическая применимость"
    )
    avg_teaching_effectiveness = models.FloatField(
        default=None,
        null=True,
        verbose_name="Эффективность преподавания"
    )
    avg_materials_availability = models.FloatField(
        default=None,
        null=True,
        verbose_name="Доступность учебных материалов"
    )
    avg_feedback_support = models.FloatField(
        default=None,
        null=True,
        verbose_name="Обратная связь и поддержка"
    )
    
    teachers = models.ManyToManyField(
        'Lecturer',
        related_name='disciplines',
        verbose_name='Преподаватели'
    )
    description = models.TextField(verbose_name='Описание дисциплины')

    class Meta:
        verbose_name = "Дисциплина"
        verbose_name_plural = "Дисциплины"

    def __str__(self):
        return self.name



    