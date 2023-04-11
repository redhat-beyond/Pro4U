from django.db import migrations, transaction


class Migration(migrations.Migration):
    dependencies = [
        ('SearchHistory', '0001_initial'),
    ]

    def generate_data(apps, schema_editor):
        from SearchHistory.models import SearchHistory

        test_data = [
            ('1', 'Test Pro1', 'Test Client1'),
            ('2', 'Test Pro2', 'Test Client2'),
            ('3', 'Test Pro3', 'Test Client3'),
            ('4', 'Test Pro4', 'Test Client4'),
        ]

        with transaction.atomic():
            for search_ID, professional_ID, client_ID in test_data:
                SearchHistory(search_ID=search_ID, professional_ID=professional_ID, client_ID=client_ID).save()

    operations = [
        migrations.RunPython(generate_data),
    ]
