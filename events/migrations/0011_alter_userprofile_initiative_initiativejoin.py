# Generated by Django 5.1 on 2024-10-21 06:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_charity_userprofile_initiative'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='initiative',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='participants', to='events.charity'),),
            
        migrations.CreateModel(
            name='InitiativeJoin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('charity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.charity')),
            ],
        ),
    ]
