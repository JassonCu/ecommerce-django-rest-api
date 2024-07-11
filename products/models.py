from django.db import models
from datetime import datetime
from category.models import Category
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Nomber'))
    description = models.TextField(verbose_name=_('Descripción'))
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=_('Precio'))
    compare_price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=_('Precio de comparación'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('Categoría'))
    quantity = models.IntegerField(default=0, verbose_name=_('Cantidad'))
    sold = models.IntegerField(default=0, verbose_name=_('Vendidos'))
    date_created = models.DateTimeField(default=datetime.now, verbose_name=_('Fecha de creación'))

    def __str__(self):
        return self.name
