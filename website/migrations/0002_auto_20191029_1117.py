# Generated by Django 2.0 on 2019-10-29 10:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Catégorie'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Produit'},
        ),
    ]
