from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    parent = models.ForeignKey(
        'self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(
        _('Nombre de categoría'), max_length=255, unique=True)

    def __str__(self):
        return self.name
