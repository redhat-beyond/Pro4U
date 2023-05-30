from django.urls import reverse
from reservation.models import TypeOfJob
from reservation.forms import TypeOfJobForm
import pytest


@pytest.fixture
def save_type_of_job(make_typeOfJob):
    typeOfJob = make_typeOfJob()
    typeOfJob.professional_id.save()
    typeOfJob.save()
    return typeOfJob


@pytest.mark.django_db
class TestTypeOfJob:
    def test_typeOfJob_list(self, client, professional, make_typeOfJob):
        typeOfJob = make_typeOfJob()
        client.force_login(professional.profile_id.user_id)
        response = client.get(reverse('typeOfJob'))
        assert response.status_code == 200
        assert 'reservation/typeOfJob_list.html' in response.templates[0].name
        assert any(typeOfJob.pk == existed_typeOfJob.pk for existed_typeOfJob in response.context['typeOfjobs_by_pro'])

    def test_create_typeOfJob(self, client, professional, save_type_of_job):
        client.force_login(professional.profile_id.user_id)
        response = client.get(reverse('typeOfJob_create'))
        assert response.status_code == 200
        assert 'reservation/typeOfJob_form.html' in response.templates[0].name

        data = {
            'typeOfJob_name': 'Woman haircut',
            'price': 200,
        }

        response = client.post(reverse('typeOfJob_create'), data)
        assert response.status_code == 302
        assert TypeOfJob.objects.filter(professional_id=professional).count() == 2
        assert response.url == reverse('typeOfJob')

    def test_typeOfJob_update(self, client, professional, save_type_of_job):
        client.force_login(professional.profile_id.user_id)
        url = reverse('typeOfJob_update', args=[save_type_of_job.pk])
        response = client.get(url)
        assert response.status_code == 200

        data = {
            'typeOfJob_name': 'Updated Type of Job',
            'price': 150,
        }

        response = client.post(url, data)
        assert response.status_code == 302
        save_type_of_job.refresh_from_db()
        assert save_type_of_job.typeOfJob_name == 'Updated Type of Job'
        assert save_type_of_job.price == 150
        assert TypeOfJob.objects.filter(professional_id=professional).count() == 1
        assert response.url == reverse('typeOfJob')

    def test_typeOfJob_delete(self, client, professional, save_type_of_job):
        client.force_login(professional.profile_id.user_id)
        url = reverse('typeOfJob_delete', args=[save_type_of_job.pk])
        response = client.post(url)
        assert response.status_code == 302
        assert TypeOfJob.objects.filter(professional_id=professional).count() == 0

    def test_form_validity(self):
        data = {
            'typeOfJob_name': 'Woman haircut',
            'price': 200,
        }

        form = TypeOfJobForm(data)
        assert form.is_valid()
