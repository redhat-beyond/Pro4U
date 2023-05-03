from django.db import migrations, transaction
from datetime import timedelta
from django.utils import timezone
from account.models.professional import Professional
from account.models.client import Client


class Migration(migrations.Migration):
    dependencies = [
        ('reservation', '0002_alter_appointment_client_id_and_more'),
        ('account', '0002_test_data'),
    ]

    def generate_data(apps, schema_editor):
        from reservation.models import Schedule, Appointment, TypeOfJob

        current_datetime = timezone.now()
        schedule_test_data = [
            (1, 1, (current_datetime + timedelta(days=3)).replace(hour=14, minute=0, second=0, microsecond=0),
             (current_datetime + timedelta(days=3)).replace(hour=19, minute=0, second=0, microsecond=0), 60),
            (2, 1, (current_datetime + timedelta(days=5)).replace(hour=14, minute=0, second=0, microsecond=0),
             (current_datetime + timedelta(days=5)).replace(hour=20, minute=0, second=0, microsecond=0), 60),
            (3, 2, (current_datetime + timedelta(days=3)).replace(hour=14, minute=0, second=0, microsecond=0),
             (current_datetime + timedelta(days=3)).replace(hour=19, minute=0, second=0, microsecond=0), 60),
            (4, 2, (current_datetime + timedelta(days=5)).replace(hour=14, minute=0, second=0, microsecond=0),
             (current_datetime + timedelta(days=5)).replace(hour=20, minute=0, second=0, microsecond=0), 60),
        ]

        typeOfJob_test_data = [
            (1, 1, "man haircut", 70),
            (2, 1, "woman haircut", 100),
            (3, 2, "Gel nail polish", 80),
        ]

        appointment_test_data = [
            (1, 1, 2, 2, (current_datetime + timedelta(days=3)).replace(hour=15, minute=0, second=0, microsecond=0),
             (current_datetime + timedelta(days=3)).replace(hour=16, minute=0, second=0, microsecond=0), ""),
            (2, 3, 2, 2, (current_datetime + timedelta(days=3)).replace(hour=16, minute=0, second=0, microsecond=0),
             (current_datetime + timedelta(days=3)).replace(hour=17, minute=0, second=0, microsecond=0), ""),
            (3, 2, 1, 1, (current_datetime + timedelta(days=3)).replace(hour=18, minute=0, second=0, microsecond=0),
             (current_datetime + timedelta(days=3)).replace(hour=19, minute=0, second=0, microsecond=0), ""),
        ]

        with transaction.atomic():
            for schedule_id, professional_id, start_day, end_day, meeting_time in schedule_test_data:
                Schedule(
                    schedule_id=schedule_id,
                    professional_id=Professional.objects.get(pk=professional_id),
                    start_day=start_day,
                    end_day=end_day,
                    meeting_time=meeting_time
                ).save()

            for typeOfJob_id, professional_id, typeOfJob_name, price in typeOfJob_test_data:
                TypeOfJob(
                    typeOfJob_id=typeOfJob_id,
                    professional_id=Professional.objects.get(pk=professional_id),
                    typeOfJob_name=typeOfJob_name,
                    price=price
                ).save()

            for appointment_id, professional_id, client_id, typeOfJob_id, start_appointment, end_appointment, summary \
                    in appointment_test_data:
                Appointment(
                    appointment_id=appointment_id,
                    professional_id=Professional.objects.get(pk=professional_id),
                    client_id=Client.objects.get(pk=client_id),
                    typeOfJob_id=TypeOfJob.objects.get(pk=typeOfJob_id),
                    start_appointment=start_appointment,
                    end_appointment=end_appointment,
                    summary=summary
                ).save()

    operations = [
        migrations.RunPython(generate_data),
    ]
