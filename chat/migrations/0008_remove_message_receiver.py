# Generated by Django 5.0 on 2023-12-20 15:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0007_remove_chat_partner_chat_partners'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='receiver',
        ),
    ]
