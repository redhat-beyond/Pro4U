from reservation.models import TypeOfJob
import pytest

TYPEOFJOB_NAME = "Hair cut"
PRICE = 100


def save_type_of_job(typeOfJob: TypeOfJob):
    typeOfJob.professional_id.save()
    typeOfJob.save()


@pytest.fixture
def persisted_type_of_job_pool(make_typeOfJob, professional):
    typeOfJob1 = make_typeOfJob()
    typeOfJob2 = make_typeOfJob(professional_id=professional, typeOfJob_name="Gel nail polish", price=90)
    save_type_of_job(typeOfJob1)
    save_type_of_job(typeOfJob2)
    return [(typeOfJob1.typeOfJob_name, typeOfJob1.price),
            (typeOfJob2.typeOfJob_name, typeOfJob2.price)]


@pytest.mark.django_db()
class TestTypeOfJobModel:
    def test_new_typeOfJob(self, make_typeOfJob, professional):
        typeOfJob = make_typeOfJob()
        assert typeOfJob.professional_id == professional
        assert typeOfJob.typeOfJob_name == TYPEOFJOB_NAME
        assert typeOfJob.price == PRICE

    def test_persist_typeOfJob(self, make_typeOfJob):
        typeOfJob = make_typeOfJob()
        assert typeOfJob in TypeOfJob.objects.all()

    def test_del_typeOfJob(self, make_typeOfJob):
        typeOfJob = make_typeOfJob()
        typeOfJob.delete()
        assert typeOfJob not in TypeOfJob.objects.all()

    def test_delete_ref_professional(self, make_typeOfJob):
        typeOfJob = make_typeOfJob()
        typeOfJob.professional_id.delete()
        assert typeOfJob not in TypeOfJob.objects.all()

    def test_get_typeofjobs_name_and_price_by_professional(self, persisted_type_of_job_pool, professional):
        assert persisted_type_of_job_pool == \
               list(TypeOfJob.get_typeofjobs_name_and_price(professional_id=professional))
