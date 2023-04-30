from reservation.models import TypeOfJob
import pytest

TYPEOFJOB_NAME = "Gel nail polish"
PRICE = 90


@pytest.fixture
def persisted_typeOfJob(typeOfJob):
    typeOfJob.professional_id.save()
    typeOfJob.save()
    return typeOfJob


@pytest.fixture
def persisted_type_of_job_pool(persisted_typeOfJob, professional):
    typeOfJob_object = TypeOfJob(professional_id=professional, typeOfJob_name="Hair cut", price=100)
    typeOfJob_object.professional_id.save()
    typeOfJob_object.save()
    return [(persisted_typeOfJob.typeOfJob_name, persisted_typeOfJob.price),
            (typeOfJob_object.typeOfJob_name, typeOfJob_object.price)]


@pytest.mark.django_db()
class TestTypeOfJobModel:
    def test_new_typeOfJob(self, typeOfJob, professional):
        assert typeOfJob.professional_id == professional
        assert typeOfJob.typeOfJob_name == TYPEOFJOB_NAME
        assert typeOfJob.price == PRICE

    def test_persist_typeOfJob(self, persisted_typeOfJob):
        assert persisted_typeOfJob in TypeOfJob.objects.all()

    def test_del_typeOfJob(self, persisted_typeOfJob):
        persisted_typeOfJob.delete()
        assert persisted_typeOfJob not in TypeOfJob.objects.all()

    def test_delete_ref_professional(self, persisted_typeOfJob):
        persisted_typeOfJob.professional_id.delete()
        assert persisted_typeOfJob not in TypeOfJob.objects.all()

    def test_get_typeofjobs_name_and_price_by_professional(self, persisted_type_of_job_pool, professional):
        assert persisted_type_of_job_pool == \
               list(TypeOfJob.get_typeofjobs_name_and_price(professional_id=professional))
