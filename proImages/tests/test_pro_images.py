import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from proImages.models import Images


IMAGE_NAME = "test_image.jpg"
IMAGE_UPLOAD = SimpleUploadedFile(IMAGE_NAME, b"binary_data")
LIKES = 100


@pytest.fixture
def image(professional):
    return Images(professional_id=professional, image=IMAGE_UPLOAD, likes=LIKES)


@pytest.fixture
def persisted_image(image, professional):
    images_object = Images(
        professional_id=professional,
        image=SimpleUploadedFile("test_image1.jpg", b"binary_data"),
        likes=50
        )
    image.save()
    images_object.save()
    return [(image.image, image.likes), (images_object.image, images_object.likes)]


@pytest.mark.django_db()
class TestImagesModel:
    def test_create_image(self, image, professional):
        assert image.professional_id == professional
        assert image.image == IMAGE_NAME
        assert image.likes == LIKES

    def test_persisted_image(self, image):
        image.save()
        assert image in Images.objects.all()

    def test_delete_image(self, image):
        image.save()
        image.delete()
        assert image not in Images.objects.all()

    def test_get_all_professional_images(self, persisted_image, professional):
        assert persisted_image == \
               list(Images.get_all_professional_images(professional_id=professional))
