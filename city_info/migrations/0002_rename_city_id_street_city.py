# Generated by Django 4.0.4 on 2022-05-27 11:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('city_info', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='street',
            old_name='city_id',
            new_name='city',
        ),
    ]
