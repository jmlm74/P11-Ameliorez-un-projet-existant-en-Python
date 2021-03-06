# Generated by Django 3.0.8 on 2020-07-21 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products_app', '0009_auto_20200721_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='bookmark',
            field=models.ManyToManyField(blank=True, default=None, related_name='products', through='products_app.Bookmark', to='products_app.Product'),
        ),
    ]
