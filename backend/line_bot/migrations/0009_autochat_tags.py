# Generated by Django 5.1.2 on 2024-10-19 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('line_bot', '0008_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='autochat',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='auto_chats', to='line_bot.tag'),
        ),
    ]
