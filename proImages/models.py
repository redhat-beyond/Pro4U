from django.db import models


class Images(models.Model):
    image_id = models.BigAutoField(primary_key=True)
    professional_id = models.PositiveIntegerField()
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    likes = models.PositiveIntegerField()

    class Meta:
        db_table = 'Images'
