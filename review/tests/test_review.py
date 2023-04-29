import pytest
from review.models import Review
from django.template.backends import django


@pytest.mark.django_db
class TestReview:
    def test_get_new_review(self, create_review) -> None:
        review = create_review()
        assert review in Review.objects.all()

    def test_get_deleted_review(self, create_review) -> None:
        review = create_review()
        Review.objects.filter(id=review.id).delete()
        assert review not in Review.objects.all()

    def test_method_filter_by_professional(self, create_review) -> None:
        review = create_review()
        filtered_reviews = Review.filter_by_professional(professional=review.professional)
        filtered_reviews_lst = list(filtered_reviews)

        if isinstance(review, Review):
            assert filtered_reviews_lst == [review]
        elif isinstance(review, django.db.models.query.QuerySet):
            assert filtered_reviews_lst == [*review]
        else:
            error_msg = "review type is neither Review or django.db.models.query.QuerySet"
            with pytest.raises(TypeError, match=error_msg):
                raise TypeError("review type is neither Review or django.db.models.query.QuerySet")

        assert len(filtered_reviews_lst) == 1

    def test_method_get_professional_avg_rating(self, create_review) -> None:
        review = create_review()
        assert Review.get_professional_avg_rating(professional=review.professional) == 4.0

    def test_method_str(self, create_review) -> None:
        review = str(create_review())
        assert "Review: #" in review  # Review number
        assert ", by 'testfirstname testlastname'" in review  # Review by
        assert "for 'testfirstname testlastname':" in review  # Review on
        assert "Creating a test review (★★★★☆ (4/5))" in review  # Review description
