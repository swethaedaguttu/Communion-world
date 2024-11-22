# Generated by Django 4.2.5 on 2024-11-22 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_alter_conversationattachment_file_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversationattachment',
            name='file',
            field=models.FileField(default=0.001092353525322741, upload_to='attachments/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='helpalert',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='help_alerts/'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(default='default.jpg', upload_to='profile_pictures/'),
        ),
    ]
