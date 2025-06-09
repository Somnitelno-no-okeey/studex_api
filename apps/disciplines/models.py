from django.db import models
from apps.common.models import BaseModel


class DisciplineFormat(models.TextChoices):
    TRADITIONAL = 'TRADITIONAL', 'Традиционная'
    ONLINE = 'ONLINE', 'Онлайн'
    BLENDED = 'BLENDED', 'Смешанная'


class ControlType(models.TextChoices):
    EXAM = 'EXAM', 'Экзамен'
    CREDIT = 'CREDIT', 'Зачет'


class Module(BaseModel):
    name = models.CharField(max_length=100, verbose_name='Название модуля')

    class Meta:
        verbose_name = "Модуль"
        verbose_name_plural = "Модули"

    def __str__(self):
        return self.name


class Discipline(BaseModel):
    name = models.CharField(max_length=255, verbose_name='Название')
    module = models.ForeignKey(
        'Module',
        on_delete=models.PROTECT,
        verbose_name='Модуль',
        related_name='disciplines'
    )

    avg_rating = models.FloatField(null=True, blank=True, verbose_name='Общая оценка')
    review_count = models.IntegerField(default=0, verbose_name='Количество отзывов')

    format = models.CharField(
        max_length=11,
        choices=DisciplineFormat.choices,
        verbose_name='Формат проведения'
    )
    control_type = models.CharField(
        max_length=10,
        choices=ControlType.choices,
        verbose_name='Тип контроля'
    )

    avg_interest = models.FloatField(default=None, null=True, verbose_name="Интересность дисциплины")
    avg_complexity = models.FloatField(default=None, null=True, verbose_name="Уровень сложности")

    avg_usefulness = models.FloatField(default=None, null=True, verbose_name="Полезность содержания")
    is_usefulness_active = models.BooleanField(default=False)

    avg_workload = models.FloatField(default=None, null=True, verbose_name="Объем нагрузки")
    is_workload_active = models.BooleanField(default=False)

    avg_logical_structure = models.FloatField(default=None, null=True, verbose_name="Логичность структуры")
    is_logical_structure_active = models.BooleanField(default=False)

    avg_practical_applicability = models.FloatField(default=None, null=True, verbose_name="Практическая применимость")
    is_practical_applicability_active = models.BooleanField(default=False)

    avg_teaching_effectiveness = models.FloatField(default=None, null=True, verbose_name="Эффективность преподавания")
    is_teaching_effectiveness_active = models.BooleanField(default=False)

    avg_materials_availability = models.FloatField(default=None, null=True, verbose_name="Доступность учебных материалов")
    is_materials_availability_active = models.BooleanField(default=False)

    avg_feedback_support = models.FloatField(default=None, null=True, verbose_name="Обратная связь и поддержка")
    is_feedback_support_active = models.BooleanField(default=False)

    teachers = models.ManyToManyField(
        'Lecturer',
        related_name='disciplines',
        verbose_name='Преподаватели'
    )

    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = "Дисциплина"
        verbose_name_plural = "Дисциплины"

    def __str__(self):
        return self.name


class Lecturer(BaseModel):
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=150, blank=True, null=True, verbose_name='Отчество')

    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"

    def get_full_name(self):
        parts = [self.last_name, self.first_name]
        if self.patronymic:
            parts.append(self.patronymic)
        return ' '.join(parts)

    def __str__(self):
        return self.get_full_name()
