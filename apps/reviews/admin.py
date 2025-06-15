from django.contrib import admin
from django import forms
from .models import Review
from apps.disciplines.models import Discipline


class ReviewAdminForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Если редактируем существующий объект
        if self.instance and self.instance.pk:
            discipline = self.instance.discipline
            self._hide_inactive_fields(discipline)
    
    def _hide_inactive_fields(self, discipline):
        """Скрывает неактивные поля критериев"""
        criteria_fields = {
            'interest': discipline.is_interest_active if hasattr(discipline, 'is_interest_active') else True,
            'complexity': discipline.is_complexity_active if hasattr(discipline, 'is_complexity_active') else True,
            'usefulness': discipline.is_usefulness_active,
            'workload': discipline.is_workload_active,
            'logical_structure': discipline.is_logical_structure_active,
            'practical_applicability': discipline.is_practical_applicability_active,
            'teaching_effectiveness': discipline.is_teaching_effectiveness_active,
            'materials_availability': discipline.is_materials_availability_active,
            'feedback_support': discipline.is_feedback_support_active,
        }
        
        for field_name, is_active in criteria_fields.items():
            if not is_active and field_name in self.fields:
                # Скрываем поле, но не удаляем его полностью
                self.fields[field_name].widget = forms.HiddenInput()
                self.fields[field_name].required = False


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    form = ReviewAdminForm
    list_display = ('user', 'discipline', 'avg_rating', 'anonymous')
    list_filter = ('discipline', 'anonymous')
    search_fields = ('user__username', 'discipline__name')
    readonly_fields = ('avg_rating', 'discipline', 'user')  # Добавляем discipline и user в readonly
    
    # Убираем возможность создавать новые отзывы через админку
    def has_add_permission(self, request):
        return False
    
    def get_fieldsets(self, request, obj=None):
        """Динамически формируем fieldsets в зависимости от активных критериев"""
        # Только для редактирования существующих объектов
        if not obj:
            return []
        
        basic_fieldset = ('Основная информация', {
            'fields': ('discipline', 'user', 'anonymous', 'comment')
        })
        
        discipline = obj.discipline
        
        # Формируем список активных критериев
        all_criteria = [
            ('interest', getattr(discipline, 'is_interest_active', True)),
            ('complexity', getattr(discipline, 'is_complexity_active', True)),
            ('usefulness', discipline.is_usefulness_active),
            ('workload', discipline.is_workload_active),
            ('logical_structure', discipline.is_logical_structure_active),
            ('practical_applicability', discipline.is_practical_applicability_active),
            ('teaching_effectiveness', discipline.is_teaching_effectiveness_active),
            ('materials_availability', discipline.is_materials_availability_active),
            ('feedback_support', discipline.is_feedback_support_active),
        ]
        
        criteria_fields = [field_name for field_name, is_active in all_criteria if is_active]
        
        criteria_fieldset = ('Оценка по критериям', {
            'fields': criteria_fields
        }) if criteria_fields else None
        
        result_fieldset = ('Результат', {
            'fields': ('avg_rating',),
            'description': 'Это поле рассчитывается автоматически из активных критериев'
        })
        
        fieldsets = [basic_fieldset]
        if criteria_fieldset:
            fieldsets.append(criteria_fieldset)
        fieldsets.append(result_fieldset)
        
        return fieldsets