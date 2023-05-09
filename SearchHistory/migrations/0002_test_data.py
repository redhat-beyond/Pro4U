from django.db import migrations, transaction


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_test_data'),
        ('SearchHistory', '0001_initial'),
        ('SearchHistory', '0002_alter_searchhistory_client_id_and_more'),
    ]

    def generate_data(apps, schema_editor):
        from SearchHistory.models import SearchHistory
        from account.models.professional import Professional
        from account.models.client import Client

        test_data = [
            ('1', Professional.filter_by_professional_id(1)[0],
             Client.filter_by_client_id(2)[0]),
            ('2', Professional.filter_by_professional_id(1)[0],
             Client.filter_by_client_id(2)[0]),
            ('3', Professional.filter_by_professional_id(1)[0],
             Client.filter_by_client_id(2)[0]),
            ('4', Professional.filter_by_professional_id(1)[0],
             Client.filter_by_client_id(2)[0]),
        ]

        with transaction.atomic():
            for search_id, professional_id, client_id in test_data:
                SearchHistory(search_id=search_id,
                              professional_id=professional_id,
                              client_id=client_id).save()

    operations = [
        migrations.RunPython(generate_data),
    ]
