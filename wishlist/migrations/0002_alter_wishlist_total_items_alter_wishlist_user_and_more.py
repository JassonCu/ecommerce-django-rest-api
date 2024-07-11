# Generated by Django 5.0.6 on 2024-07-11 18:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_product_category_alter_product_compare_price_and_more'),
        ('wishlist', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlist',
            name='total_items',
            field=models.IntegerField(default=0, verbose_name='Total de items'),
        ),
        migrations.AlterField(
            model_name='wishlist',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
        migrations.AlterField(
            model_name='wishlistitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product', verbose_name='Producto'),
        ),
        migrations.AlterField(
            model_name='wishlistitem',
            name='wishlist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wishlist.wishlist', verbose_name='Lista de deseos'),
        ),
    ]
