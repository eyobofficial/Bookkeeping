# Generated by Django 3.2.7 on 2021-10-13 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_auto_20210718_1458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solditem',
            name='unit',
            field=models.CharField(choices=[('kg', 'kg'), ('hg', 'hg'), ('dag', 'dag'), ('g', 'g'), ('dg', 'dg'), ('cg', 'cg'), ('mg', 'mg'), ('lb', 'lb'), ('in', 'in'), ('yd', 'yd'), ('mt', 'mt'), ('ft', 'ft'), ('ct', 'ct'), ('lt', 'lt'), ('cup', 'cup'), ('pt', 'pt'), ('gal', 'gal'), ('bbl', 'bbl'), ('pc', 'pc')], default='pc', help_text='Measurement unit.', max_length=3),
        ),
    ]