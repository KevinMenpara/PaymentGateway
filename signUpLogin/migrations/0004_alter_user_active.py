# Generated by Django 5.1 on 2024-08-16 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signUpLogin', '0003_user_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
