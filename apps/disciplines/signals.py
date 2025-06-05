from django.db.models import Avg
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.reviews.models import Review

def update_discipline_ratings(discipline):
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
    
    if reviews.exists():
        for field in rating_fields:
            avg_value = reviews.exclude(**{field: None}) \
                            .aggregate(avg=Avg(field))['avg']
            setattr(discipline, f'avg_{field}', avg_value)
        
        non_null_ratings = [
            getattr(discipline, f'avg_{field}') 
            for field in rating_fields 
            if getattr(discipline, f'avg_{field}') is not None
        ]
        
        discipline.avg_rating = sum(non_null_ratings) / len(non_null_ratings) if non_null_ratings else None
    else:
        for field in rating_fields:
            setattr(discipline, f'avg_{field}', None)
        discipline.avg_rating = None
    
    discipline.save()

@receiver(post_save, sender=Review)
def review_post_save(sender, instance, created, **kwargs):
    update_discipline_ratings(instance.discipline)

@receiver(post_delete, sender=Review)
def review_post_delete(sender, instance, **kwargs):
    update_discipline_ratings(instance.discipline)
    