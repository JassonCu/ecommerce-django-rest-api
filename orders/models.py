from django.db import models
from products.models import Product
from .countries import Countries
from datetime import datetime
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

# Create your models here.

User = get_user_model()

class Order(models.Model):
    class OrderStatus(models.TextChoices):
        not_processed = 'not_processed'
        processed = 'processed'
        shipping = 'shipped'
        delivered = 'delivered'
        cancelled = 'cancelled'

    status = models.CharField(
        max_length=50, choices=OrderStatus.choices, default=OrderStatus.not_processed, verbose_name=_('Estado'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Usuario'))
    transaction_id = models.CharField(max_length=255, unique=True, verbose_name=_('ID de transacción'))
    amount = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_('Monto'))
    full_name = models.CharField(max_length=255, verbose_name=_('Nombre completo'))
    address_line_1 = models.CharField(max_length=255, verbose_name=_('Dirección 1'))
    address_line_2 = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Dirección 2'))
    city = models.CharField(max_length=255, verbose_name=_('Ciudad'))
    state_province_region = models.CharField(max_length=255, verbose_name=_('Departamento'))
    postal_zip_code = models.CharField(max_length=20, verbose_name=_('Código postal'))
    country_region = models.CharField(
        max_length=255, choices=Countries.choices, default=Countries.Guatemala, verbose_name=_('País'))
    telephone_number = models.CharField(max_length=255, verbose_name=_('Teléfono'))
    shipping_name = models.CharField(max_length=255, verbose_name=_('Nombre de envío'))
    shipping_time = models.CharField(max_length=255, verbose_name=_('Tiempo de envío'))
    shipping_price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_('Precio de envío'))
    date_issued = models.DateTimeField(default=datetime.now, verbose_name=_('Fecha de emisión'))

    def __str__(self):
        return self.transaction_id


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, verbose_name=_('Producto'))
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name=_('Pedido'))
    name = models.CharField(max_length=255, verbose_name=_('Nombre'))
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_('Precio'))
    count = models.IntegerField(verbose_name=_('Cantidad'))
    date_added = models.DateTimeField(default=datetime.now, verbose_name=_('Fecha de adición'))

    def __str__(self):
        return self.name
