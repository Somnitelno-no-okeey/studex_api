from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'discipline', 'avg_rating', 'anonymous')
    list_filter = ('discipline', 'anonymous')
    search_fields = ('user__username', 'discipline__name')

    readonly_fields = ('avg_rating',)

    fieldsets = (
        ('Основная информация', {
            'fields': ('discipline', 'user', 'anonymous', 'comment')
        }),
        ('Оценка по критериям', {
            'fields': (
                'interest',
                'complexity',
                'usefulness',
                'workload',
                'logical_structure',
                'practical_applicability',
                'teaching_effectiveness',
                'materials_availability',
                'feedback_support',
            )
        }),
        ('Результат', {
            'fields': ('avg_rating',),
            'description': 'Это поле рассчитывается автоматически из активных критериев'
        })
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        discipline = None
        if obj:
            discipline = obj.discipline

        elif request.GET.get("discipline"):
            from apps.disciplines.models import Discipline
            try:
                discipline = Discipline.objects.get(id=request.GET['discipline'])

            except Discipline.DoesNotExist:
                discipline = None

        if discipline is not None:
            for field_name in ['interest', 'complexity', 'usefulness', 'workload',
                                'logical_structure', 'practical_applicability',
                                'teaching_effectiveness', 'materials_availability',
                                'feedback_support']:
                is_active = getattr(discipline, f'is_{field_name}_active', False)
                if not is_active and field_name in form.base_fields:
                    form.base_fields.pop(field_name)

        return form
