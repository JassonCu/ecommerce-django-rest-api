from django.db import models
from django.conf import settings
from orders.countries import Countries
from django.utils.translation import gettext_lazy as _

User = settings.AUTH_USER_MODEL

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,  verbose_name=_('Usuario'))
    address_line_1 = models.CharField(max_length=255, default='', verbose_name=_('Dirección 1'))
    address_line_2 = models.CharField(max_length=255, default='', verbose_name=_('Dirección 2'))
    city = models.CharField(max_length=255, default='', verbose_name=_('Ciudad'))
    state_province_region = models.CharField(max_length=255, default='', verbose_name=_('Departamento'))
    zipcode = models.CharField(max_length=20, default='', verbose_name=_('Código postal'))
    phone = models.CharField(max_length=255, default='', verbose_name=_('Teléfono'))
    country_region = models.CharField(
        max_length=255, choices=Countries.choices, default=Countries.Guatemala, verbose_name=_('País'))

    def __str__(self):
        return self.user