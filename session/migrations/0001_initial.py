# Generated by Django 5.0.4 on 2024-04-13 11:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0003_student_uid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('start_at', models.DateTimeField(auto_now_add=True)),
                ('end_at', models.DateTimeField()),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.admin')),
                ('students', models.ManyToManyField(blank=True, to='accounts.student')),
            ],
        ),
    ]
