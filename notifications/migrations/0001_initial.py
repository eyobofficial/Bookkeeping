# Generated by Django 3.1.7 on 2021-06-14 20:47

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('business', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('notification_type', models.CharField(help_text='Category or the notication.', max_length=255)),
                ('action_message', models.TextField()),
                ('action_url', models.URLField(blank=True, help_text='URL for the action resource.', null=True)),
                ('action_date', models.DateTimeField(blank=True, help_text='Date and time for taking the action.', null=True)),
                ('action_date_label', models.CharField(default='Date & time', help_text='Label to display for the action date.', max_length=255)),
                ('is_seen', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('business_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='business.businessaccount')),
            ],
            options={
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notifications',
                'ordering': ('is_seen', '-created_at'),
            },
        ),
    ]
