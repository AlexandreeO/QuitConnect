# Generated by Django 5.0.2 on 2024-04-03 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='name',
            field=models.CharField(default=1, max_length=100),
        ),
        migrations.AlterField(
            model_name='userpost',
            name='content',
            field=models.CharField(max_length=1000),
        ),
    ]
