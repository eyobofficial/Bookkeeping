# Generated by Django 3.1.7 on 2021-06-11 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_auto_20210611_2349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sold',
            name='sales_date',
            field=models.DateField(auto_now=True, help_text='last sales date'),
        ),
    ]