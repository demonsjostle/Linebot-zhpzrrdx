# Generated by Django 5.1.2 on 2024-10-24 11:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('line_bot', '0012_gptconfig'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gptconfig',
            options={'verbose_name_plural': 'ตั้งค่า GPT'},
        ),
    ]
