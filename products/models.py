from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import json

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('PERFUME', 'Perfume'),
        ('EDT', 'Eau de Toilette'),
        ('EDC', 'Eau de Cologne'),
        ('EDP', 'Eau de Parfum'),
        ('BODY_SPRAY', 'Body Spray'),
        ('LOTION', 'Loción Corporal'),
        ('CREAM', 'Crema'),
        ('GEL', 'Gel'),
        ('DEODORANT', 'Desodorante'),
        ('OTHER', 'Otro'),
    ]

    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('U', 'Unisex'),
    ]

    FRAGRANCE_CHOICES = [
        ('FLORAL', 'Floral'),
        ('ORIENTAL', 'Oriental'),
        ('WOODY', 'Amaderado'),
        ('FRESH', 'Fresco'),
        ('CITRUS', 'Cítrico'),
        ('FRUITY', 'Frutal'),
        ('SPICY', 'Especiado'),
        ('AQUATIC', 'Acuático'),
        ('GOURMAND', 'Gourmand'),
        ('OTHER', 'Otro'),
    ]

    # Información básica
    name = models.CharField(max_length=200, verbose_name="Nombre")
    brand = models.CharField(max_length=100, verbose_name="Marca", default='Sin Marca')
    description = models.TextField(verbose_name="Descripción")

    # Categorización
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name="Categoría", default='OTHER')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Género", default='U')
    fragrance_type = models.CharField(max_length=20, choices=FRAGRANCE_CHOICES, verbose_name="Tipo de Fragancia", blank=True)

    # Presentación
    volume = models.IntegerField(verbose_name="Volumen (ml)", help_text="Volumen en mililitros", default=100)

    # Inventario y precios
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo", default=0, help_text="Costo de adquisición")
    quantity = models.IntegerField(verbose_name="Cantidad en Stock")
    min_stock = models.IntegerField(verbose_name="Stock Mínimo", default=5, help_text="Alerta cuando el stock sea menor o igual a este valor")

    # Identificadores
    sku = models.CharField(max_length=100, unique=True, verbose_name="SKU")
    barcode = models.CharField(max_length=50, verbose_name="Código de Barras", blank=True)

    # Proveedor
    supplier = models.CharField(max_length=200, verbose_name="Proveedor", blank=True)

    # Imagen
    image = models.ImageField(upload_to='products/', verbose_name="Imagen", blank=True, null=True)

    # Fecha de vencimiento
    expiration_date = models.DateField(verbose_name="Fecha de Vencimiento", blank=True, null=True)

    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.brand} ({self.volume}ml)"

    @property
    def is_low_stock(self):
        """Verifica si el stock está bajo"""
        return self.quantity <= self.min_stock

    @property
    def profit_margin(self):
        """Calcula el margen de ganancia"""
        if self.cost > 0:
            return ((self.price - self.cost) / self.cost) * 100
        return 0


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


class Sale(models.Model):
    """Modelo para registrar las ventas realizadas"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario que realizó la venta")
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total de la venta")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de venta")
    ticket_number = models.CharField(max_length=50, unique=True, verbose_name="Número de ticket")

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ['-created_at']

    def __str__(self):
        return f"Venta #{self.ticket_number} - ${self.total}"

    def get_items_count(self):
        """Retorna el número total de items en la venta"""
        return self.items.aggregate(total=models.Sum('quantity'))['total'] or 0


class SaleItem(models.Model):
    """Modelo para los items individuales de cada venta"""
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items', verbose_name="Venta")
    product_name = models.CharField(max_length=200, verbose_name="Nombre del producto")
    product_brand = models.CharField(max_length=100, verbose_name="Marca")
    product_sku = models.CharField(max_length=100, verbose_name="SKU")
    quantity = models.IntegerField(verbose_name="Cantidad")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio unitario")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Subtotal")

    class Meta:
        verbose_name = "Item de Venta"
        verbose_name_plural = "Items de Venta"

    def __str__(self):
        return f"{self.product_name} x{self.quantity}"
