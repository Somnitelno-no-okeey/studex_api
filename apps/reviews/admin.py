from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'discipline', 'interest', 'complexity', 'created_at')
    list_filter = ('discipline', 'created_at')
    search_fields = ('user__username', 'discipline__name')

    def get_readonly_fields(self, request, obj=None):
        readonly = []

        if obj:
            discipline = obj.discipline
            flag_fields = {
                'usefulness': getattr(discipline, 'is_usefulness_active', True),
                'workload': getattr(discipline, 'is_workload_active', True),
                'logical_structure': getattr(discipline, 'is_logical_structure_active', True),
                'practical_applicability': getattr(discipline, 'is_practical_applicability_active', True),
                'teaching_effectiveness': getattr(discipline, 'is_teaching_effectiveness_active', True),
                'materials_availability': getattr(discipline, 'is_materials_availability_active', True),
                'feedback_support': getattr(discipline, 'is_feedback_support_active', True),
            }
            for field, is_active in flag_fields.items():
                if not is_active:
                    readonly.append(field)

        return readonly

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        if obj:
            discipline = obj.discipline
            flag_fields = {
                'usefulness': getattr(discipline, 'is_usefulness_active', True),
                'workload': getattr(discipline, 'is_workload_active', True),
                'logical_structure': getattr(discipline, 'is_logical_structure_active', True),
                'practical_applicability': getattr(discipline, 'is_practical_applicability_active', True),
                'teaching_effectiveness': getattr(discipline, 'is_teaching_effectiveness_active', True),
                'materials_availability': getattr(discipline, 'is_materials_availability_active', True),
                'feedback_support': getattr(discipline, 'is_feedback_support_active', True),
            }
            for field, is_active in flag_fields.items():
                if not is_active and field in form.base_fields:
                    form.base_fields[field].disabled = True

        return form
