from django.db import migrations, transaction


class Migration(migrations.Migration):
    dependencies = [
        ('chatmessage', '0001_initial'),
    ]

    def generate_data(apps, schema_editor):
        from chatmessage.models import Chatmessage

        test_data = [
            ('1', 'Test Pro1', 'Test Client1', 'A simple test message1'),
            ('2', 'Test Pro2', 'Test Client2', 'A simple test message2'),
            ('3', 'Test Pro3', 'Test Client3', 'A simple test message3'),
            ('4', 'Test Pro4', 'Test Client4', 'A simple test message4'),
        ]

        with transaction.atomic():
            for message_id, professional_id, client_id, message in test_data:
                Chatmessage(message_id=message_id, professional_id=professional_id,
                            client_id=client_id, message=message).save()

    operations = [
        migrations.RunPython(generate_data),
    ]
