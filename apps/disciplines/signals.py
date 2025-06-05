from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from apps.reviews.models import Review

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
        avg_value = reviews.exclude(**{f'avg_{field}__isnull': True}) \
                           .aggregate(avg=Avg(f'avg_{field}'))['avg']
        setattr(discipline, f'avg_{field}', avg_value)

    non_null_avgs = [
        getattr(discipline, f'avg_{field}') for field in rating_fields
        if getattr(discipline, f'avg_{field}') is not None
    ]
    discipline.avg_rating = sum(non_null_avgs) / len(non_null_avgs) if non_null_avgs else None
    discipline.review_count = reviews.count()

    discipline.save(update_fields=[f'avg_{field}' for field in rating_fields] + ['avg_rating', 'review_count'])
