# Generated by Django 5.1 on 2024-10-21 06:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_culturalstory'),
    ]

    operations = [
        migrations.CreateModel(
            name='Charity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('location', models.CharField(max_length=255)),
                ('founder_name', models.CharField(max_length=255)),
                ('founder_email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.AddField(
            model_name='userprofile',
            name='initiative',
            field=models.ForeignKey(default=0.0010375494071146246, on_delete=django.db.models.deletion.CASCADE, related_name='participants', to='events.charity'),
            preserve_default=False,
        ),
    ]
