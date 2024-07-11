from products.models import Product
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

User = settings.AUTH_USER_MODEL

class WishList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('Usuario'))
    total_items = models.IntegerField(default=0, verbose_name=_('Total de items'))


class WishListItem(models.Model):
    wishlist = models.ForeignKey(WishList, on_delete=models.CASCADE, verbose_name=_('Lista de deseos'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Producto'))