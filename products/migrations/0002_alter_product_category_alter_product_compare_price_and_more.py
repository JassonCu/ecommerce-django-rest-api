# Generated by Django 5.0.6 on 2024-07-11 18:19

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category.category', verbose_name='Categoría'),
        ),
        migrations.AlterField(
            model_name='product',
            name='compare_price',
            field=models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Precio de comparación'),
        ),
        migrations.AlterField(
            model_name='product',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='Fecha de creación'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(verbose_name='Descripción'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Nomber'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Precio'),
        ),
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(default=0, verbose_name='Cantidad'),
        ),
        migrations.AlterField(
            model_name='product',
            name='sold',
            field=models.IntegerField(default=0, verbose_name='Vendidos'),
        ),
    ]
