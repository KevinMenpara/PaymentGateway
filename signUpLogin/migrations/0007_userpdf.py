# Generated by Django 5.1 on 2024-08-17 18:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signUpLogin', '0006_user_last_login'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPDF',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf_file', models.FileField(upload_to='user_pdfs/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='signUpLogin.user')),
            ],
        ),
    ]
