from django.db import migrations, transaction
from datetime import datetime


class Migration(migrations.Migration):
    dependencies = [
        ('reservation', '0001_initial'),
    ]

    def generate_data(apps, schema_editor):
        from reservation.models import Schedule
        test_data = [
            (1, 1, datetime(2023, 4, 16, 14, 00, 0), datetime(2023, 4, 16, 19, 00, 0), 60),
            (2, 1, datetime(2023, 4, 19, 14, 00, 0), datetime(2023, 4, 19, 20, 00, 0), 60),
            (3, 2, datetime(2023, 4, 16, 14, 00, 0), datetime(2023, 4, 16, 19, 00, 0), 60),
            (4, 2, datetime(2023, 4, 19, 14, 00, 0), datetime(2023, 4, 19, 20, 00, 0), 60),
        ]
        with transaction.atomic():
            for schedule_id, professional_id, start_day, end_day, meeting_time in test_data:
                Schedule(
                    schedule_id=schedule_id,
                    professional_id=professional_id,
                    start_day=start_day,
                    end_day=end_day,
                    meeting_time=meeting_time
                ).save()

    def generate_data2(apps, schema_editor):
        from reservation.models import TypeOfJob
        test_data = [
            (1, 1, "man haircut", 70),
            (2, 1, "woman haircut", 100),
            (3, 2, "Gel nail polish", 80),
        ]
        with transaction.atomic():
            for typeOfJob_id, professional_id, typeOfJob_name, price in test_data:
                TypeOfJob(
                    typeOfJob_id=typeOfJob_id,
                    professional_id=professional_id,
                    typeOfJob_name=typeOfJob_name,
                    price=price
                ).save()

    def generate_data3(apps, schema_editor):
        from reservation.models import Appointment, TypeOfJob
        test_data = [
            (1, 1, 1, 1, datetime(2023, 4, 16, 15, 00, 0), datetime(2023, 4, 16, 16, 00, 0), ""),
            (2, 1, 2, 2, datetime(2023, 4, 16, 16, 00, 0), datetime(2023, 4, 16, 17, 00, 0), ""),
            (3, 2, 1, 1, datetime(2023, 4, 16, 18, 00, 0), datetime(2023, 4, 16, 19, 00, 0), ""),
        ]
        with transaction.atomic():
            for appointment_id, professional_id, client_id, typeOfJob_id, start_appointment, end_appointment, summary \
                                                                                                        in test_data:
                Appointment(
                    appointment_id=appointment_id,
                    professional_id=professional_id,
                    client_id=client_id,
                    typeOfJob_id=TypeOfJob.objects.get(pk=typeOfJob_id),
                    start_appointment=start_appointment,
                    end_appointment=end_appointment,
                    summary=summary
                ).save()

    operations = [
        migrations.RunPython(generate_data),
        migrations.RunPython(generate_data2),
        migrations.RunPython(generate_data3),
    ]
