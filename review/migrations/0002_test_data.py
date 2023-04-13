from django.db import migrations, transaction


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0001_initial'),
    ]

    def generate_data(apps, schema_editor):
        from review.models import Review, Rating
        from django.contrib.auth.models import User

        user1 = User.objects.create_user(username='example_user1', email='user1@example.com', password='password')
        user2 = User.objects.create_user(username='example_user2', email='user2@example.com', password='password')

        test_data = [
            (user1, Rating.UNSPECIFIED, "2011-09-01T13:20:30+03:00", 'A simple test review'),
            (user2, Rating.FIVE_STARS,  "2011-09-01T13:20:30+03:00", 'Another simple test review'),
        ]

        with transaction.atomic():
            for author, rating, date_posted, description in test_data:
                Review(author=author, rating=rating, date_posted=date_posted, description=description).save()

    operations = [
        migrations.RunPython(generate_data),
    ]
