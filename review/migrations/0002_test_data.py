from datetime import timedelta

from django.db import migrations, transaction
from django.utils import timezone

from account.models.client import Client
from account.models.professional import Professional


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0001_initial'),
        ('account', '0002_test_data'),
    ]

    def generate_data(apps, schema_editor):
        from review.models import Review

        now = timezone.now()

        # Generate review data
        review_test_data = [
            ('5', 'Excellent!', now - timedelta(days=10), 1, 1),
            ('4', 'Good', now - timedelta(days=20), 2, 2),
            ('3', 'Average', now - timedelta(days=5), 3, 3),
            ('2', 'A simple test review', now - timedelta(days=2), 1, 3),
            (Review.Rating.FOUR_STARS, 'Another test review', now - timedelta(days=2), 3, 2),
            (Review.Rating.ONE_STAR, 'Really bad.', now - timedelta(days=2), 3, 2),
        ]
        # Create review
        with transaction.atomic():
            for rating, description, date_posted, client_id, professional_id in review_test_data:
                Review(
                    rating=rating,
                    description=description,
                    date_posted=date_posted,
                    client=Client.objects.get(pk=client_id),
                    professional=Professional.objects.get(pk=professional_id)
                ).save()

    operations = [
        migrations.RunPython(generate_data),
    ]
