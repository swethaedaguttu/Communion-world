# Generated by Django 5.1 on 2024-10-07 11:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_activity'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=100)),
                ('feedback_date', models.DateTimeField(auto_now_add=True)),
                ('feedback_text', models.TextField()),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to='events.community')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='events.community')),
            ],
        ),
        migrations.CreateModel(
            name='Partnership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('partner_name', models.CharField(max_length=100)),
                ('partnership_date', models.DateField()),
                ('description', models.TextField()),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partnerships', to='events.community')),
            ],
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('link', models.URLField()),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resources', to='events.community')),
            ],
        ),
        migrations.CreateModel(
            name='SupportRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=100)),
                ('request_date', models.DateTimeField(auto_now_add=True)),
                ('request_details', models.TextField()),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='support_requests', to='events.community')),
            ],
        ),
    ]
