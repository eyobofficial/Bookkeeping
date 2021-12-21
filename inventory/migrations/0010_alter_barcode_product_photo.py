# Generated by Django 3.2.7 on 2021-12-21 10:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shared', '0003_auto_20210808_1146'),
        ('inventory', '0009_barcode_product_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='barcode',
            name='product_photo',
            field=models.OneToOneField(blank=True, help_text='A foreign key to the Photo Upload object.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='barcode_product_photo', to='shared.photoupload'),
        ),
    ]
