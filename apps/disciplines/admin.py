from django.contrib import admin
from .models import Discipline, Lecturer, Module


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    list_display = ('name', 'module', 'format', 'control_type')
    list_filter = ('format', 'control_type', 'module')
    search_fields = ('name',)

    fieldsets = (
        (None, {
            'fields': (
                'name',
                'module',
                'format',
                'control_type',
                'description',
                'teachers',
            )
        }),
        ('Дополнительные критерии (включение/отключение)', {
            'fields': (
                ('is_usefulness_active',),
                ('is_workload_active',),
                ('is_logical_structure_active',),
                ('is_practical_applicability_active',),
                ('is_teaching_effectiveness_active',),
                ('is_materials_availability_active',),
                ('is_feedback_support_active',),
            )
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['is_usefulness_active'].label = 'Добавить критерий "Полезность содержания"'
        form.base_fields['is_workload_active'].label = 'Добавить критерий "Объем нагрузки"'
        form.base_fields['is_logical_structure_active'].label = 'Добавить критерий "Логичность структуры"'
        form.base_fields['is_practical_applicability_active'].label = 'Добавить критерий "Практическая применимость"'
        form.base_fields['is_teaching_effectiveness_active'].label = 'Добавить критерий "Эффективность преподавания"'
        form.base_fields['is_materials_availability_active'].label = 'Добавить критерий "Доступность учебных материалов"'
        form.base_fields['is_feedback_support_active'].label = 'Добавить критерий "Обратная связь и поддержка"'
        return form


@admin.register(Lecturer)
class LecturerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'patronymic')
    fields = ('first_name', 'last_name', 'patronymic')


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fields = ('name',)
