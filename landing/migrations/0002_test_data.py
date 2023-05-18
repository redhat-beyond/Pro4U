from django.db import migrations, transaction

from landing.models import TeamMember


class Migration(migrations.Migration):
    dependencies = [
        ('landing', '0001_initial'),
    ]

    def generate_data(apps, schema_editor):
        test_data = [
            'Guy Beckenstein',
            'Ido Singer',
            'Ido Yekutiel',
            'Ofir Bachar',
            'Patrisia Kaplun',
            'Tal Reinfeld',
        ]
        with transaction.atomic():
            for name in test_data:
                name_without_whitespaces = ''.join(name.split())
                TeamMember(
                    name=name,
                    img=f'/img/{name_without_whitespaces}.jpg',
                    alt=name_without_whitespaces,
                ).save()

    operations = [
        migrations.RunPython(generate_data),
    ]
