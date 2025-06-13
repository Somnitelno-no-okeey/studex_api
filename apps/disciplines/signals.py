from django.db.models import Avg
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.reviews.models import Review
from apps.disciplines.models import Discipline

@receiver([post_save, post_delete], sender=Review)
def update_discipline_ratings(sender, instance, **kwargs):
    discipline = instance.discipline
    reviews = discipline.reviews.all()

    rating_fields = [
        'interest',
        'complexity',
        'usefulness',
        'workload',
        'practical_applicability',
        'logical_structure',
        'teaching_effectiveness',
        'materials_availability',
        'feedback_support'
    ]

    for field in rating_fields:
        avg_value = reviews.exclude(**{f'{field}__isnull': True}) \
                           .exclude(**{field: 0}) \
                           .aggregate(avg=Avg(field))['avg']
        setattr(discipline, f'avg_{field}', avg_value)


    active_avg_fields = []
    values = []
    for field in rating_fields:
        flag_field = f'is_{field}_active'
        if not hasattr(discipline, flag_field) or getattr(discipline, flag_field, True):
            avg_field = f'avg_{field}'
            active_avg_fields.append(avg_field)
            val = getattr(discipline, avg_field)
            if val is not None:
                values.append(val)

    discipline.avg_rating = sum(values) / len(values) if values else None
    discipline.review_count = reviews.count()

    discipline.save(update_fields=active_avg_fields + ['avg_rating', 'review_count'])
