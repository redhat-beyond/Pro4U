from django.db import models


class Images(models.Model):
    images_ID = models.BigAutoField(primary_key=True)
    # professional_ID = models.ForeignKey(Professional, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    likes = models.PositiveIntegerField()

    class Meta:
        db_table = 'Images'
