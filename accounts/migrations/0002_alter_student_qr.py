# Generated by Django 5.0.4 on 2024-04-12 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='qr',
            field=models.ImageField(blank=True, upload_to='students/qr/'),
        ),
    ]
