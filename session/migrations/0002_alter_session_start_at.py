# Generated by Django 5.0.4 on 2024-04-13 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='start_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
