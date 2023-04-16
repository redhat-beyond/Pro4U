from django.db import migrations, transaction, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0001_initial'),
    ]

    def generate_data(apps, schema_editor):
        from review.models import Review, Rating

        test_data = [
            ("user1", "pro1", Rating.UNSPECIFIED, "2011-09-01T13:20:30+03:00", 'A simple test review'),
            ("user2", "pro1", Rating.FIVE_STARS,  "2011-09-01T13:20:30+03:00", 'Another simple test review'),
        ]

        with transaction.atomic():
            for client_id, professional_id, rating, date_posted, description in test_data:
                Review(
                    rating=rating,
                    description=description,
                    date_posted=date_posted,
                    client_id=client_id,
                    professional_id=professional_id
                ).save()

    operations = [
        migrations.AddField(
            model_name='review',
            name='client_id',
            field=models.CharField(max_length=512),
        ),
        migrations.RunPython(generate_data),
    ]
