from django.db import models
from account.models.professional import Professional


class Images(models.Model):
    image_id = models.BigAutoField(primary_key=True)
    professional_id = models.ForeignKey(Professional, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    likes = models.PositiveIntegerField()

    class Meta:
        db_table = 'Images'

    @staticmethod
    def get_all_professional_images(professional_id: int):
        images_list = Images.objects.filter(professional_id=professional_id)\
                                    .values_list('image', 'likes')
        return images_list
