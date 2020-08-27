# Generated by Django 3.0.8 on 2020-07-21 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products_app', '0005_auto_20200721_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='fat',
            field=models.CharField(choices=[('H', 'Elevé'), ('M', 'Modéré'), ('L', 'Bas'), ('U', 'Inconnu')], default='U', max_length=1, verbose_name='Lipides'),
        ),
        migrations.AlterField(
            model_name='product',
            name='salt',
            field=models.CharField(choices=[('H', 'Elevé'), ('M', 'Modéré'), ('L', 'Bas'), ('U', 'Inconnu')], default='U', max_length=1, verbose_name='Sel'),
        ),
        migrations.AlterField(
            model_name='product',
            name='saturated_fat',
            field=models.CharField(choices=[('H', 'Elevé'), ('M', 'Modéré'), ('L', 'Bas'), ('U', 'Inconnu')], default='U', max_length=1, verbose_name='Acides gras satures'),
        ),
        migrations.AlterField(
            model_name='product',
            name='sugar',
            field=models.CharField(choices=[('H', 'Elevé'), ('M', 'Modéré'), ('L', 'Bas'), ('U', 'Inconnu')], default='U', max_length=1, verbose_name='Sucres'),
        ),
    ]
