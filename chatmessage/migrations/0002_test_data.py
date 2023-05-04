from django.db import migrations, transaction


class Migration(migrations.Migration):
    dependencies = [
        ('account', '0002_test_data'),
        ('chatmessage', '0001_initial'),
        ('chatmessage', '0002_chatmessage_sender_type_alter_chatmessage_client_id_and_more'),
    ]

    def generate_data(apps, schema_editor):
        from chatmessage.models import Chatmessage, SenderType
        from account.models.professional import Professional
        from account.models.client import Client

        test_data = [
            (Professional.filter_by_professional_id(1)[0], Client.filter_by_client_id(2)[0],
             'A simple test message1', SenderType.Client),
            (Professional.filter_by_professional_id(1)[0], Client.filter_by_client_id(2)[0],
             'A simple test message2', SenderType.Client),
            (Professional.filter_by_professional_id(1)[0], Client.filter_by_client_id(2)[0],
             'A simple test message3', SenderType.Professional),
            (Professional.filter_by_professional_id(1)[0], Client.filter_by_client_id(2)[0],
             'A simple test message4', SenderType.Professional),
        ]

        with transaction.atomic():
            for professional_id, client_id, message, sender_type in test_data:
                Chatmessage(professional_id=professional_id,
                            client_id=client_id, message=message, sender_type=sender_type).save()

    operations = [
        migrations.RunPython(generate_data),
    ]
