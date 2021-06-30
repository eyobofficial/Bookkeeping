# Generated by Django 3.1.7 on 2021-06-30 09:10

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customers', '0001_initial'),
        ('inventory', '0001_initial'),
        ('business', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('order_type', models.CharField(choices=[('FROM_LIST', 'from list'), ('CUSTOM', 'custom order')], max_length=10)),
                ('description', models.TextField(blank=True, help_text='Required for `CUSTOM` order types to describe the sold items.', null=True)),
                ('custom_cost', models.DecimalField(blank=True, decimal_places=2, help_text='A total price offer for custom order.', max_digits=10, null=True)),
                ('status', models.CharField(choices=[('OPEN', 'Open'), ('CLOSED', 'Closed')], default='OPEN', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('business_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='business.businessaccount')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='customers.customer')),
            ],
            options={
                'verbose_name': 'Customer Order',
                'verbose_name_plural': 'Customer Orders',
                'ordering': ('-created_at',),
                'default_related_name': 'orders',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='inventory.stock')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='orders.order')),
            ],
            options={
                'verbose_name': 'Order Item',
                'verbose_name_plural': 'Order Items',
                'ordering': ('updated_at',),
                'default_related_name': 'order_items',
            },
        ),
    ]
