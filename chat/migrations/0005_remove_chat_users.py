# Generated by Django 5.0 on 2023-12-17 15:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_chat_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='users',
        ),
    ]