# Generated by Django 4.2 on 2023-04-30 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SearchHistory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searchhistory',
            name='client_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.client'),
        ),
        migrations.AlterField(
            model_name='searchhistory',
            name='professional_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.professional'),
        ),
    ]
