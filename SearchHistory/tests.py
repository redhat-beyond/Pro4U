from SearchHistory.models import SearchHistory
import pytest
# from django.db.models import Max


@pytest.fixture
def persisted_search_history(searchHistory):
    searchHistory.save()
    return [(searchHistory.search_id), (searchHistory.professional_id),
            (searchHistory.client_id), (searchHistory.date)]


@pytest.mark.django_db
class TestSearchHistoryModel:
    def test_new_member(self, searchHistory, professional, demo_client):
        assert searchHistory.professional_id == professional
        assert searchHistory.client_id == demo_client

    def test_search_history(self, searchHistory):
        searchHistory.save()
        assert searchHistory in SearchHistory.objects.all()

    def test_del_search_history(self, searchHistory):
        searchHistory.save()
        searchHistory.delete()
        assert searchHistory not in SearchHistory.objects.all()

    def test_get_last_professionals_search_by_client(self, persisted_search_history, demo_client, expected_result=5):
        expected_professionals = SearchHistory.objects.filter(client_id=demo_client).order_by('-date')[:expected_result]
        result = SearchHistory.get_last_professionals_search_by_client(persisted_search_history[2])
        assert sorted(result) == sorted(expected_professionals)
