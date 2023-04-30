from django.db import migrations, transaction
from account.models.professional import Professional


class Migration(migrations.Migration):
    dependencies = [
        ('proImages', '0002_alter_images_professional_id'),
        ('account', '0002_test_data'),
    ]

    def generate_data(apps, schema_editor):
        from proImages.models import Images

        test_data = [
            (1, 1, '', 100),
            (2, 2, '', 200),
            (3, 3, '', 300),
            (4, 4, '', 400),
        ]

        with transaction.atomic():
            for image_id, professional_id, image, likes in test_data:
                Images(
                    image_id=image_id,
                    professional_id=Professional.objects.get(pk=professional_id),
                    image=image, likes=likes
                    ).save()

    operations = [
        migrations.RunPython(generate_data),
    ]
