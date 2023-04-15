# Generated by Django 4.1.7 on 2023-04-14 16:32

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('client_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('birthday', models.DateField(default=datetime.date(2000, 1, 1), verbose_name='Birthday')),
                ('profile_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user.profile')),
            ],
            options={
                'db_table': 'client',
            },
        ),
    ]
