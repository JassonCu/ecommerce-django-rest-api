from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class FixedPriceCoupon(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_('Nombre'))
    discount_price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_('Precio de descuento'))

    def __str__(self):
        return self.name


class PercentageCoupon(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_('Nombre'))
    discount_percentage = models.IntegerField(verbose_name=_('Porcentaje de descuento'))

    def __str__(self):
        return self.name