# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from apps.reviews.models import Review

# @receiver([post_save, post_delete], sender=Review)
# def update_review_avg_rating(sender, instance, **kwargs):
#     rating_fields = [
#         'avg_interest',
#         'avg_complexity',
#         'avg_usefulness',
#         'avg_workload',
#         'avg_practical_applicability',
#         'avg_logical_structure',
#         'avg_teaching_effectiveness',
#         'avg_materials_availability',
#         'avg_feedback_support'
#     ]
    
#     values = [
#         getattr(instance, field)
#         for field in rating_fields
#         if getattr(instance, field) is not None
#     ]
#     instance.avg_rating = sum(values) / len(values) if values else None
#     instance.save(update_fields=['avg_rating'])
