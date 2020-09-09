# Generated by Django 3.1 on 2020-09-07 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products_app', '0011_auto_20200722_1906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='fat',
            field=models.CharField(choices=[('H', 'high'), ('M', 'moderate'), ('L', 'low'), ('U', 'unknown')], default='U', max_length=1, verbose_name='Lipides'),
        ),
        migrations.AlterField(
            model_name='product',
            name='salt',
            field=models.CharField(choices=[('H', 'high'), ('M', 'moderate'), ('L', 'low'), ('U', 'unknown')], default='U', max_length=1, verbose_name='Sel'),
        ),
        migrations.AlterField(
            model_name='product',
            name='saturated_fat',
            field=models.CharField(choices=[('H', 'high'), ('M', 'moderate'), ('L', 'low'), ('U', 'unknown')], default='U', max_length=1, verbose_name='Acides gras satures'),
        ),
        migrations.AlterField(
            model_name='product',
            name='sugar',
            field=models.CharField(choices=[('H', 'high'), ('M', 'moderate'), ('L', 'low'), ('U', 'unknown')], default='U', max_length=1, verbose_name='Sucres'),
        ),
    ]
