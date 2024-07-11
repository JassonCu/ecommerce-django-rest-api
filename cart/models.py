from django.db import models
from products.models import Product
from django.conf import settings
from django.utils.translation import gettext_lazy as _

User = settings.AUTH_USER_MODEL

# Create your models here.

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('Usuario'))
    total_items = models.IntegerField(default=0, verbose_name=_('Total de items'))


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name=_('Carrito'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Producto'))
    count = models.IntegerField(verbose_name=_('Cantidad'))