from datetime import timedelta
from django.db import migrations, transaction
from django.utils import timezone


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0001_initial'),
    ]

    def generate_data(apps, schema_editor):
        from review.models import Review

        now = timezone.now()

        test_data = [
            ('5', 'Excellent!', now - timedelta(days=10), 'user1', 'pro1'),
            ('4', 'Good', now - timedelta(days=20), 'user2', 'pro2'),
            ('3', 'Average', now - timedelta(days=5), 'user3', 'pro3'),
            ('2', 'A simple test review', now - timedelta(days=2), 'user1', 'pro3'),
            (Review.Rating.FOUR_STARS, 'Another test review', now - timedelta(days=2), 'user3', 'pro2'),
            (Review.Rating.ONE_STAR, 'Really bad.', now - timedelta(days=2), 'user3', 'pro2'),
        ]

        with transaction.atomic():
            for rating, description, date_posted, client_id, professional_id in test_data:
                Review(
                    rating=rating,
                    description=description,
                    date_posted=date_posted,
                    client_id=client_id,
                    professional_id=professional_id
                ).save()

    operations = [
        migrations.RunPython(generate_data),
    ]
