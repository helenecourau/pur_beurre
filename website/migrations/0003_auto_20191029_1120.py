# Generated by Django 2.0 on 2019-10-29 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_auto_20191029_1117'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='name',
            new_name='name_cat',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='name',
            new_name='name_prod',
        ),
    ]
