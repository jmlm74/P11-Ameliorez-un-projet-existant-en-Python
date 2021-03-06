# Generated by Django 3.0.8 on 2020-07-22 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products_app', '0010_auto_20200721_1942'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookmark',
            options={},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['nutriscore_grade'], 'verbose_name': 'Product', 'verbose_name_plural': 'Product'},
        ),
        migrations.AddIndex(
            model_name='bookmark',
            index=models.Index(fields=['buser'], name='I_buser'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['nutriscore_grade'], name='I_nutriscore_grade'),
        ),
        migrations.AddConstraint(
            model_name='bookmark',
            constraint=models.UniqueConstraint(fields=('product', 'substitute', 'buser'), name='unique_bookmark'),
        ),
        migrations.AddConstraint(
            model_name='productswish',
            constraint=models.UniqueConstraint(fields=('pwname',), name='unique_pwname'),
        ),
    ]
