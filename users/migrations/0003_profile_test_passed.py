# Generated by Django 4.1.3 on 2022-12-11 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='test_passed',
            field=models.BooleanField(default=False),
        ),
    ]
