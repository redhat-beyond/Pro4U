from account.models.professional import Professional
from django.urls import reverse
import pytest

CLIENT_ID = 2


@pytest.mark.django_db
def test_search_page(client):
    url = reverse('search history', args=[CLIENT_ID])
    response = client.get(url)
    assert response.status_code == 200
    assert 'html/search.html' in response.templates[0].name


@pytest.mark.django_db
def test_search_by_no_filters(client):
    url = reverse('search history', args=[CLIENT_ID])

    response = client.post(url, {})
    professionals = response.context['professionals']
    assert list(professionals) == list(Professional.objects.all())


@pytest.mark.django_db
def test_search_by_professional_id(client, make_professional):
    professional = make_professional()
    url = reverse('search history', args=[CLIENT_ID])
    data = {
            'professional_id': professional.professional_id,
            'opened': '0',
        }
    response = client.post(url, data)

    assert response.status_code == 200
    assert 'html/search.html' in response.templates[0].name

    professionals = response.context['professionals']
    assert len(professionals) == 1
    assert professionals[0].professional_id == professional.professional_id
    assert professionals[0].profession == professional.profession
    assert professionals[0].profile_id.user_id.first_name == professional.profile_id.user_id.first_name
    assert professionals[0].profile_id.user_id.last_name == professional.profile_id.user_id.last_name
    assert professionals[0].profile_id.city == professional.profile_id.city
