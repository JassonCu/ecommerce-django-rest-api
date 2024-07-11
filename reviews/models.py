from datetime import datetime
from products.models import Product
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Create your models here.

User = settings.AUTH_USER_MODEL


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Usuario'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Producto'))
    rating = models.DecimalField(max_digits=2, decimal_places=1, verbose_name=_('Calificación'))
    comment = models.TextField(verbose_name=_('Comentario'))
    date_created = models.DateTimeField(default=datetime.now, verbose_name=_('Fecha de creación'))

    def __str__(self):
        return self.comment