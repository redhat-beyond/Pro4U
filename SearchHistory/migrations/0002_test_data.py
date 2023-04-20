from datetime import timedelta
from django.db import migrations, transaction
from django.utils import timezone


class Migration(migrations.Migration):

    dependencies = [
        ('SearchHistory', '0001_initial'),
    ]

    def generate_data(apps, schema_editor):
        from SearchHistory.models import SearchHistory

        now = timezone.now()

        test_data = [
            ('1', '101', '601',  now - timedelta(days=10)),
            ('2', '102', '602',  now - timedelta(days=20)),
            ('3', '103', '603',  now - timedelta(days=12)),
            ('4', '104', '604',  now - timedelta(days=100)),
        ]

        with transaction.atomic():
            for search_id, professional_id, client_id, date in test_data:
                SearchHistory(search_id=search_id,
                              professional_id=professional_id,
                              client_id=client_id,
                              date=date).save()

    operations = [
        migrations.RunPython(generate_data),
    ]
