# Generated by Django 3.1.7 on 2021-05-20 20:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='business',
            new_name='business_account',
        ),
    ]