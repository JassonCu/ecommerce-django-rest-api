from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Shipping(models.Model):
    class Meta:
        verbose_name = 'Shipping'
        verbose_name_plural = 'Shipping'

    name = models.CharField(max_length=255, unique=True, verbose_name=_('Nombre'))
    time_to_delivery = models.CharField(max_length=255, verbose_name=_('Tiempo de entrega'))
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_('Precio'))

    def __str__(self):
        return self.name