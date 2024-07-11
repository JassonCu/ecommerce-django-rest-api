# Generated by Django 5.0.6 on 2024-07-11 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fixedpricecoupon',
            name='discount_price',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Precio de descuento'),
        ),
        migrations.AlterField(
            model_name='fixedpricecoupon',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='percentagecoupon',
            name='discount_percentage',
            field=models.IntegerField(verbose_name='Porcentaje de descuento'),
        ),
        migrations.AlterField(
            model_name='percentagecoupon',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='Nombre'),
        ),
    ]
