# Generated by Django 3.1.7 on 2021-05-15 23:21

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_remove_setting_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='country',
            field=django_countries.fields.CountryField(default='NG', max_length=2),
        ),
    ]
