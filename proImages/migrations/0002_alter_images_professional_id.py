# Generated by Django 4.2 on 2023-04-30 12:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_test_data'),
        ('proImages', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='professional_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.professional'),
        ),
    ]
