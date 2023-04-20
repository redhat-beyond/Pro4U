from .models import SearchHistory
from datetime import datetime
import pytest

PROFESSIONAL_ID = 101
CLIENT_ID = 601
DATE = datetime(2023, 4, 17, 10, 0, 0)


@pytest.fixture
def searchHistory():
    return SearchHistory(professional_id=PROFESSIONAL_ID, client_id=CLIENT_ID, date=DATE)


@pytest.fixture
def persisted_search_history(searchHistory):
    searchHistory.save()
    return [(searchHistory.search_id), (searchHistory.professional_id),
            (searchHistory.client_id), (searchHistory.date)]


@pytest.mark.django_db
class TestSearchHistoryModel:
    def test_new_member(self, searchHistory):
        assert searchHistory.professional_id == PROFESSIONAL_ID
        assert searchHistory.client_id == CLIENT_ID
        assert searchHistory.date == DATE

    def test_search_history(self, searchHistory):
        searchHistory.save()
        assert searchHistory in SearchHistory.objects.all()

    def test_del_search_history(self, searchHistory):
        searchHistory.save()
        searchHistory.delete()
        assert searchHistory not in SearchHistory.objects.all()

    def test_get_5_last_professionals_search_by_client(self, persisted_search_history):
        persisted_client_id = persisted_search_history[2]
        expected_result = SearchHistory.objects.filter(client_id=persisted_client_id)
        expected_result = expected_result.order_by('-date')[:5]
        expected_result = expected_result.values_list('professional_id', flat=True)
        result = SearchHistory.get_5_last_professionals_search_by_client(persisted_search_history[2])
        assert sorted(result) == sorted(expected_result)
