# Generated by Django 3.2.7 on 2021-12-12 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_unique_stock_barcode_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='barcode',
            name='created_by_api',
        ),
        migrations.AddField(
            model_name='barcode',
            name='brand_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='barcode',
            name='created_strategy',
            field=models.IntegerField(choices=[(1, 'Manually via Django Admin'), (2, 'API Calls'), (3, 'Imported from a CSV file')], default=1, help_text='The strategy used to create this record.'),
        ),
        migrations.AddField(
            model_name='barcode',
            name='manufacturer_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='barcode',
            name='product_name',
            field=models.CharField(max_length=255),
        ),
    ]
