from django import forms

from review.models import Review


class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        label="Rating",
        choices=Review.Rating.choices,
    )
    description = forms.CharField(
        label='Review description',
        widget=forms.Textarea(attrs={'placeholder': 'Write review'}),
        required=False
    )

    class Meta:
        model = Review
        fields = [
            'rating',
            'description'
        ]
