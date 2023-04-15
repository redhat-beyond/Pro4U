# Generated by Django 4.1.7 on 2023-04-14 16:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Professional',
            fields=[
                ('professional_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('profession', models.CharField(blank=True, choices=[('PLU', 'Plumber'),
                                                                     ('GAR', 'Gardener'),
                                                                     ('ELE', 'Electrician'),
                                                                     ('TIN', 'Tinsmith'),
                                                                     ('PAI', 'Painter'),
                                                                     ('LOC', 'Locksmith'),
                                                                     ('EXT', 'Exterminator'),
                                                                     ('GAT', 'GasTechnician'),
                                                                     ('ACT', 'AirConditioningTechnician'),
                                                                     ('RET', 'RefrigeratorTechnician'),
                                                                     ('CLE', 'Cleaner'),
                                                                     ('HAN', 'Handyman')], max_length=3)),
                ('description', models.TextField(blank=True)),
                ('profile_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user.profile')),
            ],
            options={
                'db_table': 'professional',
            },
        ),
    ]
