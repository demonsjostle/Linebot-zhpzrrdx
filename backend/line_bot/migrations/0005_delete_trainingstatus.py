# Generated by Django 5.1.2 on 2024-10-18 17:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('line_bot', '0004_alter_trainingstatus_progress'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TrainingStatus',
        ),
    ]