from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import json

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre")
    description = models.TextField(verbose_name="Descripción")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    quantity = models.IntegerField(verbose_name="Cantidad")
    sku = models.CharField(max_length=100, unique=True, verbose_name="SKU")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class History(models.Model):
    ACTION_CHOICES = [
        ('CREATE', 'Creación'),
        ('UPDATE', 'Edición'),
        ('DELETE', 'Eliminación'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")
    product_id = models.IntegerField(verbose_name="ID del Producto")
    product_name = models.CharField(max_length=200, verbose_name="Nombre del Producto")
    action = models.CharField(max_length=10, choices=ACTION_CHOICES, verbose_name="Acción")
    changes = models.TextField(verbose_name="Cambios", blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Fecha")

    class Meta:
        verbose_name = "Historial"
        verbose_name_plural = "Historiales"
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username} - {self.get_action_display()} - {self.product_name}"

    def get_changes_dict(self):
        if self.changes:
            try:
                return json.loads(self.changes)
            except:
                return {}
        return {}


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_admin = models.BooleanField(default=False, verbose_name="Es Administrador")

    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuario"

    def __str__(self):
        return f"{self.user.username} - {'Admin' if self.is_admin else 'Usuario'}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
