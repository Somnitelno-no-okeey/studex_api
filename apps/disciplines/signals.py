from django.db.models import Avg
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.reviews.models import Review

def update_discipline_ratings(discipline):

    reviews = discipline.reviews.all()  
    
    if reviews.exists():
        discipline.avg_interest = reviews.aggregate(avg=Avg('interest'))['avg']
        discipline.avg_complexity = reviews.aggregate(avg=Avg('complexity'))['avg']
        discipline.avg_usefulness = reviews.aggregate(avg=Avg('usefulness'))['avg']
        discipline.avg_workload = reviews.aggregate(avg=Avg('workload'))['avg']
        discipline.avg_practical_applicability = reviews.aggregate(avg=Avg('practical_applicability'))['avg']
        discipline.avg_logical_structure = reviews.aggregate(avg=Avg('logical_structure'))['avg']
        discipline.avg_teaching_effectiveness = reviews.aggregate(avg=Avg('teaching_effectiveness'))['avg']
        discipline.avg_materials_availability = reviews.aggregate(avg=Avg('materials_availability'))['avg']
        discipline.avg_feedback_support = reviews.aggregate(avg=Avg('feedback_support'))['avg']
    else:
        discipline.avg_interest = 0
        discipline.avg_complexity = 0
        discipline.avg_usefulness = 0
        discipline.avg_workload = 0
        discipline.avg_practical_applicability = 0
        discipline.avg_logical_structure = 0
        discipline.avg_teaching_effectiveness = 0
        discipline.avg_materials_availability = 0
        discipline.avg_feedback_support = 0
    
    discipline.save()

@receiver(post_save, sender=Review)
def review_post_save(sender, instance, created, **kwargs):
    update_discipline_ratings(instance.discipline)

@receiver(post_delete, sender=Review)
def review_post_delete(sender, instance, **kwargs):
    update_discipline_ratings(instance.discipline)