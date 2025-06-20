from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_place = models.CharField(max_length=255, blank=True, verbose_name='Место рождения')
    death_place = models.CharField(max_length=255, blank=True, verbose_name='Место смерти')
    latitude = models.FloatField(null=True, blank=True, verbose_name='Широта')
    longitude = models.FloatField(null=True, blank=True, verbose_name='Долгота')
    photo = models.ImageField(upload_to='profiles/', blank=True, null=True, verbose_name='Фото')
    media_archive = models.FileField(upload_to='media_archives/', blank=True, null=True, verbose_name='Медиаархив')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Профиль {self.user.username}"

# Модель для семейного древа (упрощённо)
class FamilyTree(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='family_trees')
    name = models.CharField(max_length=255)
    data = models.JSONField(default=dict, blank=True)  # Для хранения структуры древа
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Древо {self.name} ({self.owner.username})"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
